import os
from dotenv import load_dotenv
from helper import call_api
from datetime import datetime
from peewee import *
import caldav
from rich.console import Console

console = Console()

load_dotenv()

# Get the Grocy API URL and Bearer token from the environment
grocy_url = os.environ['GROCY_HOST']
grocy_token = os.environ['GROCY_TOKEN']

# Create data folder if it does not exist
if not os.path.exists('data'):
    os.makedirs('data')

db = SqliteDatabase('data/sync.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Synced(BaseModel):
    grocy_id = IntegerField()
    grocy_product_id = IntegerField()
    name = CharField()
    amount = IntegerField()
    caldav_uuid = CharField()
    datetime = DateTimeField(default=datetime.now)

def grocy_add_missing_products():
    return call_api(f"{grocy_url}/api/stock/shoppinglist/add-missing-products", grocy_api_key=grocy_token, query_type='POST', body={}) # ohne dem leeren Body 500 Error

def grocy_remove_done_items():
    return call_api(f"{grocy_url}/api/stock/shoppinglist/clear", grocy_api_key=grocy_token, query_type='POST', body={"done_only": True})

def grocy_get_items():
    return call_api(f"{grocy_url}/api/objects/shopping_list", grocy_api_key=grocy_token, query_type="GET")

def grocy_get_product(product_id):
    return call_api(f"{grocy_url}/api/stock/products/{product_id}", grocy_api_key=grocy_token, query_type="GET")

def get_caldav_list():
    with caldav.DAVClient(
        url = os.environ['CALDAV_HOST'],
        username=os.environ['CALDAV_USER'],
        password=os.environ['CALDAV_PASSWORD']
    ) as client:
        shopping_list = client.calendar(url=os.environ['CALDAV_SHOPPING_LIST_URL'])
        assert 'VTODO' in shopping_list.get_supported_components()
        return shopping_list.todos()

def insert_caldav_item(name: str, amount: int):
    with caldav.DAVClient(
        url = os.environ['CALDAV_HOST'],
        username=os.environ['CALDAV_USER'],
        password=os.environ['CALDAV_PASSWORD']
    ) as client:
        shopping_list = client.calendar(url=os.environ['CALDAV_SHOPPING_LIST_URL'])
        return shopping_list.save_todo(
            summary=f"{name} {amount}"
        )

def get_caldav_item(uid: str):
    with caldav.DAVClient(
        url = os.environ['CALDAV_HOST'],
        username=os.environ['CALDAV_USER'],
        password=os.environ['CALDAV_PASSWORD']
    ) as client:
        shopping_list = client.calendar(url=os.environ['CALDAV_SHOPPING_LIST_URL'])
        return shopping_list.search(todo=True, uid=uid)[0]

def overwrite_caldav_item(uid: str, name: str, amount: int):
    with caldav.DAVClient(
        url = os.environ['CALDAV_HOST'],
        username=os.environ['CALDAV_USER'],
        password=os.environ['CALDAV_PASSWORD']
    ) as client:
        shopping_list = client.calendar(url=os.environ['CALDAV_SHOPPING_LIST_URL'])
        item = shopping_list.search(todo=True, uid=uid)[0]
        item.instance.vtodo.summary.value = f"{name} {amount}"
        item.save()

def check_if_alrady_in_caldav(name: str, caldav_item_names: list[str]) -> list[str]:
    return [item for item in caldav_item_names if name.lower() in item.lower()]


def main():
    db.connect()
    db.create_tables([Synced])
    console.print("DB connected and initialized")

    grocy_add_missing_products()
    grocy_remove_done_items()
    console.print("Grocy prepared")

    caldav_items = get_caldav_list()
    caldav_item_names = [item.instance.vtodo.summary.value for item in caldav_items]
    console.print("CalDav prepared")

    items = grocy_get_items()
    for item in items:
        id = item['id']
        db_item = Synced.get_or_none(Synced.grocy_id == id)
        if db_item is None:
            product = grocy_get_product(item['product_id'])
            name = product['product']['name']
            console.print(f"New Item: {name} - Amount: {item['amount']}")
            already_in_caldav = check_if_alrady_in_caldav(name, caldav_item_names)
            if len(already_in_caldav) > 0:
                console.print(f"[bold red]Already in CalDav: {already_in_caldav}[/bold red]")
            console.print(f"[bold green]Adding to CalDav: {name}[/bold green]")
            caldav_item = insert_caldav_item(name, item['amount'])
            caldav_uuid = caldav_item.instance.vtodo.uid.value
            Synced.create(grocy_id=id,
                grocy_product_id=item['product_id'],
                name=name,
                amount=item['amount'],
                caldav_uuid=caldav_uuid
            )
        elif db_item.amount != item['amount']:
            console.print(f"[bold red]{db_item.name} amount changed: {db_item.amount} -> {item['amount']}[/bold red]")
            caldav_item = get_caldav_item(uid=db_item.caldav_uuid)
            print(f"Found old item: {caldav_item.instance.vtodo.summary.value}")
            overwrite_caldav_item(uid=db_item.caldav_uuid, name=db_item.name, amount=item['amount'])
            console.print(f"[bold green]Updated CalDav: {db_item.name} - Amount: {item['amount']}[/bold green]")
            db_item.amount = item['amount']
            db_item.save()


if __name__=="__main__":
    main()