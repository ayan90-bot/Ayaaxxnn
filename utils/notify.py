def notify_admins(bot, admin_ids, message):
    for admin_id in admin_ids:
        try:
            bot.send_message(admin_id, message)
        except Exception as e:
            print(f"Failed to notify {admin_id}: {e}")
