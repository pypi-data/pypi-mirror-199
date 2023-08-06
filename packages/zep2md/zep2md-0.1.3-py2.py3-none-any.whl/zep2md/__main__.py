import codecs
import json
from pathlib import Path

import numpy as np
import pandas as pd
import typer
from clumper import Clumper
from clumper.sequence import row_number

app = typer.Typer(
    name="zep2md",
    add_completion=False,
    help="This is app translates zeppelin files to markdown with syntax highlighting.",
)


# fmt: off
template = lambda language, value: f"""```{language}
{value}
```
"""
# fmt: on


@app.command()
def translate(
    source: str = typer.Argument(
        ..., help="The path to the zeppelin file that you want to translate"
    )
):
    """Minimal translation of a zeppelin file to a markdown file."""
    p = Path(source)
    sink = p.name.replace(".zpln", ".md")
    data = json.load(codecs.open(source, "r", "utf-8-sig"))

    titles = (
        Clumper(data["paragraphs"], listify=False)
        .mutate(r=row_number())
        .keep(lambda d: "title" in d.keys())
        .select("r", "title")
    )
    text = (
        Clumper(data["paragraphs"], listify=False)
        .mutate(r=row_number())
        .keep(lambda d: "text" in d.keys())
        .select("r", "text")
    )
    if len(titles) > 0:
        text = text.left_join(titles, mapping={"r": "r"}).drop("r")
    table = text.mutate(
        md=lambda d: d["text"].startswith("%md"),
        pyspark=lambda d: d["text"].startswith("%pyspark"),
        sh=lambda d: d["text"].startswith("%sh"),
        spark=lambda d: d["text"].startswith("%spark"),
        sql=lambda d: not d["text"].startswith("%"),
    ).collect()

    df = pd.DataFrame(table)

    df["text"] = df.apply(
        lambda x: np.where(
            x["pyspark"] == True, template("python", x["text"]), x["text"]
        ).tolist(),
        1,
    )
    df["text"] = df.apply(
        lambda x: np.where(
            x["spark"] == True, template("scala", x["text"]), x["text"]
        ).tolist(),
        1,
    )
    df["text"] = df.apply(
        lambda x: np.where(
            x["sh"] == True, template("bash", x["text"]), x["text"]
        ).tolist(),
        1,
    )
    df["text"] = df.apply(
        lambda x: np.where(
            x["sql"] == True, template("sql", x["text"]), x["text"]
        ).tolist(),
        1,
    )
    df["text"] = df.apply(
        lambda x: np.where(
            x["md"] == True, template("md", x["text"]), x["text"]
        ).tolist(),
        1,
    )

    if len(titles) > 0:
        df["title"] = np.where(df["title"].isna(), "", df["title"])
        df["aux"] = df["title"] + "\n\n" + df["text"] + "\n"
        aux = df["aux"].values
        aux = "\n".join([*aux])
    else:
        aux = "\n\n".join([*df["text"].values])

    with open(sink, "w") as f:
        f.write(aux)


if __name__ == "__main__":
    app()
