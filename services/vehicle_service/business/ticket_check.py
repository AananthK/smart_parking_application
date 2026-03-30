from persistence.ticket_dao import get_all_unpaid_tickets_by_driver_id, get_ticket_by_ticket_id

def ticket_exists(ticket_id: int):
    return get_ticket_by_ticket_id(ticket_id = ticket_id)

def find_unpaid_tickets(driver_id: int):
    return get_all_unpaid_tickets_by_driver_id