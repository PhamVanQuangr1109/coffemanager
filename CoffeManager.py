import csv
import json
from datetime import datetime

def load_config(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return config
    except FileNotFoundError:
        print(f"[ERR-01] Không tìm thấy file '{filename}'")
        return None

    except json.JSONDecodeError:
        print(f"[ERR-02] file '{filename}' rỗng hoặc sai định dạng.")
        return None

def load_menu(filename):
    menu = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                row['price'] = int(row['price'])
                menu.append(row)

        if len(menu) == 0:
            print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")
            return None

        return menu

    except FileNotFoundError:
        print(f"[ERR-01] Không tìm thấy file '{filename}'.")
        return None

    except (ValueError, csv.Error):
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")
        return None

def load_order(filename):
    orders=[]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line == '':
                    continue
                parts=line.split("|")
                if len(parts) != 4:
                    continue
                else:
                    time=parts[0].strip()
                    ord_id=parts[1].strip()
                    items=parts[2].strip()
                    total=parts[3].strip()

                total=int(total)

                orders.append({
                    'time': time,
                    'ord_id': ord_id,
                    'items': items,
                    'total': total
                })
        return orders
    except FileNotFoundError:
        return []

def show_menu(menu):
    print('\n========== THỰC ĐƠN ==========')

    len_id = max(len(item['id']) for item in menu) + 3
    len_name = max(len(item['name']) for item in menu) + 3
    len_category = max(len(item['category']) for item in menu) + 3

    print(
        f'{"Mã":<{len_id}}'
        f'{"Tên món":<{len_name}}'
        f'{"Loại":<{len_category}}'
        f'{"Giá":>10}'
    )

    print('-' * (len_id + len_name + len_category + 10))

    for item in menu:
        print(
            f'{item["id"]:<{len_id}}'
            f'{item["name"]:<{len_name}}'
            f'{item["category"]:<{len_category}}'
            f'{item["price"]:>10}'
        )

    print('-' * (len_id + len_name + len_category + 10))
    print(f'Tổng số món: {len(menu)}')

def find_item(menu):
    item_id=input("Nhập id món: ").strip().upper()

    for item in menu:
        if item['id'].upper()==item_id:
            return item
    return None

def show_history(orders):
    if len(orders)==0:
        print("[ERR-06] Chưa có đơn hàng nào trong lịch sử.")
        return

    print('\n========== LỊCH SỬ ĐƠN HÀNG ==========')

    len_time = max(len(order['time']) for order in orders) + 3
    len_id = max(len(order['ord_id']) for order in orders) + 3
    len_items = max(len(order['items']) for order in orders) + 3

    print(
        f"{'Thời gian':<{len_time}}"
        f"{'Mã đơn':<{len_id}}"
        f"{'Món':<{len_items}}"
        f"{'Tổng tiền':>12}"
    )

    print('-' * (len_time + len_id + len_items + 12))

    for order in orders:
        print(
            f"{order['time']:<{len_time}}"
            f"{order['ord_id']:<{len_id}}"
            f"{order['items']:<{len_items}}"
            f"{order['total']:>12}"
        )

    print('-' * (len_time + len_id + len_items + 12))

def main():
    config = load_config('config.json')
    menu = load_menu('menu.csv')
    orders = load_order('orders.txt')

    if config is None or menu is None:
        return

    while True:

        print('\n========== THE COFFEE CORNER ==========')
        print('1. Xem thực đơn')
        print('2. Tìm món theo mã')
        print('3. Tạo đơn hàng')
        print('4. Xem lịch sử đơn hàng')
        print('0. Thoát')
        print('=======================================')

        try:
            choice = int(input('Chọn chức năng: ').strip())

        except ValueError:
            print("[ERR-03] Dữ liệu nhập không hợp lệ. Vui lòng nhập số nguyên.")
            continue

       
        if choice == 0:
            print('Đã thoát chương trình.')
            break


        elif choice == 1:
            show_menu(menu)

        elif choice == 2:
            item = find_item(menu)

            if item is None:
                print("[ERR-04] Không tìm thấy món.")
            else:
                print('\n========== THÔNG TIN MÓN ==========')
                print(f"Mã: {item['id']}")
                print(f"Tên: {item['name']}")
                print(f"Loại: {item['category']}")
                print(f"Giá: {item['price']:} VND")


        elif choice == 3:
            pass

        elif choice == 4:
            show_history(orders)

        else:
            print("[ERR-03] Dữ liệu nhập không hợp lệ. Vui lòng nhập số nguyên.")

if __name__ == '__main__':
    main()