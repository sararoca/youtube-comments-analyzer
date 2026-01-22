import math

def paginate(total_items: int, page: int, page_size: int):
    
    total_pages = max(1, math.ceil(total_items / page_size))
    page = max(1, min(page, total_pages))

    offset = (page - 1) * page_size
    limit = page_size

    return {
        "page": page,
        "total_pages": total_pages,
        "offset": offset,
        "limit": limit,
    }
