# from src import Main

if __name__ == "__main__":
    # Main().start()

    from pandas import DataFrame

    df = DataFrame(data={"a": [1, 2, 3], "b": [3, 2, 1]})
    df.set_index("a", inplace=True)
    # print(df)
    # print(df.index.name)
    # print(df["b"].to_list())
    # print(df.iloc[2])
    print()
    row_len = len(df)
    for i in range(row_len):
        index = df.index[i]
        print(df.loc[index].index.to_list())
        break

    # for item in df.iterrows():
    #     print(item.index.to_list())
    #     break
