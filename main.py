from src import Main

if __name__ == "__main__":
    Main().start()


# from pandas import DataFrame, concat

# df = DataFrame(data={"a": ["1_", "2_", "3_"], "b": [3, 2, 1]})
# # df = DataFrame(columns=["a", "b"])
# df.set_index("a", inplace=True)
# filter = df.index == "2_"
# print(df[filter])


# print(df.columns)
# for i in range(len(df)):
#     print(df.iloc[i].name)
# # print(df.index.name)
# print(df)
# print(df.index.name)
# print(df["b"].to_list())
# print(df.iloc[2])

# for i in range(2):
#     temp = DataFrame(data={"a": [f"{i}__"], "b": [i]})
#     temp.set_index("a", inplace=True)
#     # print(temp)
#     # temp.set_index("a", inplace=True)
#     df = concat([df, temp])
# # df.set_index("a", inplace=True)

# print(df)

# row_len = len(df)
# for i in range(row_len):
#     index = df.iloc[i]
#     print(index["b"])
#     # print(df.loc[index], )
#     break
