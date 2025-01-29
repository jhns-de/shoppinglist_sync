from dotenv import load_dotenv
import os
import caldav
from rich.console import Console

console = Console()

load_dotenv()

with caldav.DAVClient(
    url = os.environ['CALDAV_HOST'],
    username=os.environ['CALDAV_USER'],
    password=os.environ['CALDAV_PASSWORD']
) as client:
    console.rule("Calendars")
    p = client.principal()
    cals = p.calendars()
    for c in cals:
        print(c.name, c.url)

    console.rule("Shopping List")    
    shopping_list = client.calendar(url=os.environ['CALDAV_SHOPPING_LIST_URL'])
    assert 'VTODO' in shopping_list.get_supported_components()
    items = shopping_list.todos()
    for item in items:
        print(item.instance.vtodo.summary.value)

    console.rule("Single Item")

    print(item.data)

    console.rule("Pretty Print")

    item.instance.prettyPrint()

    console.rule("Add Test Item")
    item = shopping_list.save_todo(
        summary="Test Item",
        description="This is a test item",
    )
    item.instance.prettyPrint()
    print(item.instance.vtodo.summary.value)
    print(item.instance.vtodo.uid.value)