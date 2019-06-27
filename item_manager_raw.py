import pickle

item_names = ["chocolate",
              "energy drink (bottle)",
              "energy drink (can)",
              "protein powder",
              "protein bar",
              "beef jerky",
              "non-fat yogurt",
              "milk",
              "skimmed milk",
              "spring water"]

item_price = [6,
              4.99,
              3.99,
              43.5,
              5.5,
              5.5,
              6.5,
              5.35,
              4.85,
              3.5]

item_data = [[item_names[i].title(), item_names[i].replace(' ', '_').replace('(', '').replace(')', '') + ".png", item_price[i]] for i in range(len(item_names))]

print(item_data)

with open("res/items.p", 'bw') as f:
    pickle.dump(item_data, f)
