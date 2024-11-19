def archive_order(order_id: int, db: Session):
    # Получение заказа из базы данных
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise ValueError("Order not found")

    if  not order.status :  # Проверяем, что заказ неактивен
        # Формируем данные для архива
        order_data = {
            "order_id": order.id,
            "cafeteria_id": order.cafeteria_id,
            "user_id": order.user_id,
            "order_items": [
                {"coffee_id": item.coffee_id, "quantity": item.quantity}
                for item in order.order_items
            ]
        }

        # Сохраняем данные в Redis
        redis_client.rpush(f"user:{order.user_id}:archives", json.dumps(order_data))

        print(f"Order {order.id} archived for user {order.user_id}.")
    else:
        print(f"Order {order.id} is still active and cannot be archived.")