title = ['대학', '대학1', '대학2']
a = input('')
b = list()
for index, i in enumerate(title):
    if a in title[index]:
        b.append(title[index])
    else:
        print('안맞자나', i, index)
print(b)

for index, i in enumerate(b):
    print(f'{index+1}. {i}')
c = input('숫자입력해')
d = ['1', '2', '3', '4', '5']
# if c == d[0]:
#     print(f'현재 {b[0]}에 들어왔')
# if c == d[1]:
#     print(f'현재 {b[1]}에 들어왔')
for c in d:
    if c == d:
    for 