import pandas as pd


def load_data(input_file):
    df = pd.read_csv(input_file)
    return df

def create_key(df, n):
    df = df.copy()
    df["key"] = df["text"]
    df["key"] = df["key"].str.strip()
    df["key"] = df["key"].str.lower()
    df["key"] = df["key"].str.replace("-", "")
    df["key"] = df["key"].str.translate(
        str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_´{|}~")
    )
    df["key"] = df["key"].str.split()
    df["key"] = df["key"].str.join("")
    df["key"] = df["key"].map(
        lambda x: [x[t : t+n-1] for t in range(len(x))]
    )
    df["key"] = df["key"].apply(lambda x: sorted(set(x)))
    df["key"] = df["key"].str.join("")
    return df

def generate_cleaned_column(df):
    df = df.copy()
    #df = df.sort_values(by=["key", "text"], ascending=[True, True])
    keys = df.drop_duplicates(subset="key", keep="first")
    key_dict = dict(zip(keys["key"], keys["text"]))
    df["cleaned_text"] = df["key"].map(key_dict)
    return df

def save_data(df, output_file):
    df = df.copy()
    df = df[["cleaned_text"]]
    df = df.rename(columns={"cleaned_text": "cleaned_text"})
    df = df.map(lambda x: "AD-HOC QUERIES" if x == "ADHOC QUERIES" else x)
    df.to_csv(output_file, index=False)

def main(input_file, output_file, n=3):
    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("files/test.csv", index=False)
    save_data(df, output_file)

if __name__ == "__main__":
    main(
        input_file="files/input.txt",
        output_file="files/output.txt"
    )