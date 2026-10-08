import csv
import json
from datetime import datetime
import numpy as np


def load_config(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"[ERR-01] Không tìm thấy file '{filename}'.")

    except (ValueError, OSError):
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")

    return None


def load_menu(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    except FileNotFoundError:
        print(f"[ERR-01] Không tìm thấy file '{filename}'.")

    except (csv.Error, OSError):
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")

    return None


def load_order(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.readlines()

    except FileNotFoundError:
        return []

    except OSError:
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")
        return None


def process_menu(menu, filename):
    if len(menu) == 0:
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")
        return None

    try:
        for item in menu:
            item['id']
            item['name']
            item['category']
            item['price'] = int(item['price'])

        return menu

    except (KeyError, ValueError, TypeError):
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")
        return None


def process_order(lines):
    orders = []

    for line in lines:
        parts = line.strip().split('|')

        if len(parts) != 4:
            continue

        try:
            orders.append({
                'time': parts[0].strip(),
                'ord_id': parts[1].strip(),
                'items': parts[2].strip(),
                'total': int(parts[3].strip())
            })

        except ValueError:
            continue

    return orders


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
            f'{item["price"]:>10,}'
        )

    print('-' * (len_id + len_name + len_category + 10))
    print(f'Tổng số món: {len(menu)}')


def find_item(menu):
    item_id = input('Nhập id món: ').strip().upper()

    for item in menu:
        if item['id'].upper() == item_id:
            print('\n========== THÔNG TIN MÓN ==========')
            print(f"Mã: {item['id']}")
            print(f"Tên: {item['name']}")
            print(f"Loại: {item['category']}")
            print(f"Giá: {item['price']:,} VND")
            return

    print(f"[ERR-04] Không tìm thấy món có mã '{item_id}'.")


def create_order(menu, orders, config):
    items = []
    amounts = []

    while True:
        item_id = input(
            'Nhập mã món (Enter để kết thúc): '
        ).strip().upper()

        if item_id == '':
            break

        found = None

        for item in menu:
            if item['id'].upper() == item_id:
                found = item
                break

        if found is None:
            print(f"[ERR-04] Không tìm thấy món có mã '{item_id}'.")
            continue

        while True:
            try:
                quantity = int(input('Số lượng: '))

                if quantity > 0:
                    break

            except ValueError:
                pass

            print(
                '[ERR-05] Số lượng phải là số nguyên dương. '
                'Vui lòng nhập lại.'
            )

        amount = found['price'] * quantity

        amounts.append(amount)
        items.append(f"{found['id']}x{quantity}")

        print(f"  + {found['name']} x{quantity} = {amount:,}")

    if len(items) == 0:
        print('[ERR-05] Đơn hàng chưa có món nào.')
        return

    subtotal = int(np.sum(amounts))
    discount = 0

    if subtotal >= config['discount_threshold']:
        discount = subtotal * config['discount_rate']

    vat = (subtotal - discount) * config['vat_rate']
    total = round(subtotal - discount + vat)

    print('-' * 30)
    print(f'Tạm tính  : {subtotal:>12,}')
    print(f'Giảm giá  : {discount:>12,.0f}')
    print(f"VAT ({config['vat_rate']:.0%})  : {vat:>12,.0f}")
    print(f"TỔNG CỘNG : {total:>12,} {config['currency']}")

    order = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'ord_id': f'HD{len(orders) + 1:03d}',
        'items': ', '.join(items),
        'total': total
    }

    filename = config['files']['orders']

    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(
                f"\n{order['time']} | {order['ord_id']} | "
                f"{order['items']} | {order['total']}\n"
            )

        orders.append(order)

        print(f"[OK] Đã lưu đơn {order['ord_id']} vào {filename}")

    except OSError:
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")


def show_history(orders):
    if len(orders) == 0:
        print('[ERR-06] Chưa có đơn hàng nào trong lịch sử.')
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
            f"{order['total']:>12,}"
        )

    print('-' * (len_time + len_id + len_items + 12))


def export_report(orders, menu, config):
    totals = []
    items_sold = {}

    for order in orders:
        totals.append(order['total'])

        for item in order['items'].split(','):
            try:
                item_id, quantity = item.strip().rsplit('x', 1)
                quantity = int(quantity)

            except ValueError:
                continue

            if item_id in items_sold:
                items_sold[item_id] += quantity
            else:
                items_sold[item_id] = quantity

    revenue = int(np.sum(totals))
    best_seller = None

    if len(items_sold) > 0:
        item_id = max(items_sold, key=items_sold.get)
        name = ''

        for item in menu:
            if item['id'] == item_id:
                name = item['name']
                break

        best_seller = {
            'id': item_id,
            'name': name,
            'quantity': items_sold[item_id]
        }

    report = {
        'shop_name': config['shop_name'],
        'total_orders': len(orders),
        'total_revenue': revenue,
        'items_sold': items_sold,
        'best_seller': best_seller
    }

    filename = config['files']['report']

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(
            f"[OK] Đã xuất báo cáo ra {filename} "
            f"({len(orders)} đơn, doanh thu {revenue:,} "
            f"{config['currency']})"
        )

    except OSError:
        print(f"[ERR-02] File '{filename}' rỗng hoặc sai định dạng.")


def main():
    config = load_config('config.json')

    if config is None:
        return

    try:
        menu_file = config['files']['menu']
        order_file = config['files']['orders']
        config['files']['report']
        config['shop_name']
        config['currency']
        config['vat_rate']
        config['discount_threshold']
        config['discount_rate']

    except (KeyError, TypeError):
        print("[ERR-02] File 'config.json' rỗng hoặc sai định dạng.")
        return

    menu = load_menu(menu_file)

    if menu is None:
        return

    menu = process_menu(menu, menu_file)

    if menu is None:
        return

    lines = load_order(order_file)

    if lines is None:
        return

    orders = process_order(lines)

    while True:
        print(f"\n========== {config['shop_name']} ==========")
        print('1. Xem thực đơn')
        print('2. Tìm món theo mã')
        print('3. Tạo đơn hàng')
        print('4. Xem lịch sử đơn hàng')
        print('5. Xuất báo cáo doanh thu')
        print('0. Thoát')
        print('=======================================')

        try:
            choice = int(input('Chọn chức năng: ').strip())

        except ValueError:
            print(
                '[ERR-03] Dữ liệu nhập không hợp lệ. '
                'Vui lòng nhập số nguyên.'
            )
            continue

        if choice == 0:
            print('Đã thoát chương trình.')
            break

        elif choice == 1:
            show_menu(menu)

        elif choice == 2:
            find_item(menu)

        elif choice == 3:
            create_order(menu, orders, config)

        elif choice == 4:
            lines = load_order(order_file)

            if lines is not None:
                orders = process_order(lines)
                show_history(orders)

        elif choice == 5:
            lines = load_order(order_file)

            if lines is not None:
                orders = process_order(lines)
                export_report(orders, menu, config)

        else:
            print(
                '[ERR-03] Dữ liệu nhập không hợp lệ. '
                'Vui lòng chọn từ 0 đến 5.'
            )


if __name__ == '__main__':
    main()