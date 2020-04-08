import click
import os.path
import sys
import datetime
import json

todo_folder = ".todo"
quick_folder = "internal_quick_todo_list"
todo_file = "todo.json"


todo_folder_path = os.path.expanduser(os.path.join("~", todo_folder))
quick_folder_path = os.path.join(todo_folder_path, quick_folder)


def get_topics():
    for root, dirs, files in os.walk(todo_folder_path):
        dirs[:] = [d for d in dirs if not d[0] == '.']


@click.group()
def cli():
    pass


@cli.command()
@click.option("--topic", "-t", default=quick_folder, type=click.STRING, autocompletion=get_topics)
@click.argument("todo", type=click.STRING)
def add(topic, todo) -> None:
    if (not topic_exists(topic)):
        if click.confirm("Topic doesn't exist, would you like to create one?"):
            create_topic(topic)
        else:
            exit()
    todo = create_todo(todo)
    add_todo_to_topic(todo, topic)


@cli.command()
@click.argument("topic", required=True, default=quick_folder, type=click.STRING, autocompletion=get_topics)
def view(topic: str):
    if (not topic_exists(topic)):
        click.echo("Topic doesn't exist.")
        sys.exit(1)
    todos = load_topic(topic)["todos"]

    print("Todos for topic: " + topic)
    print("==============================")
    for todo in todos:
        todo_json = json.loads(todo)
        print(todo_json["todo"])
    return


def setup() -> None:
    try:
        setup()
    except Exception as e:
        print(e)


def create_todo(todo: str) -> str:
    timestamp = datetime.datetime.now()
    complete = False
    record = {
        "timestamp": str(timestamp),
        "complete": complete,
        "todo": todo
    }
    json_record = json.dumps(record)
    return json_record


def create_directory() -> None:
    # do init things
    if not os.path.exists(todo_folder_path):
        os.mkdir(todo_folder_path)
        os.mkdir(quick_folder_path)
    else:
        raise Exception("Installation failed: " + todo_folder_path + " already exists.")


def create_topic(topic: str) -> None:
    new_topic_path = os.path.join(todo_folder_path, topic)
    if not os.path.exists(new_topic_path):
        os.mkdir(new_topic_path)
        todo_file_path = os.path.join(new_topic_path, todo_file)
        with open(todo_file_path, 'w') as f:
            default_record = {
                "todos": []
            }
            f.write(json.dumps(default_record))
    else:
        raise Exception("THIS IS A BUG! Trying to create a topic already exists.")


def topic_exists(topic: str) -> bool:
    new_topic_path = os.path.join(todo_folder_path, topic)
    return os.path.exists(new_topic_path)


def load_topic(topic: str) -> str:
    topic_path = os.path.join(todo_folder_path, topic)
    topic_todo_file = os.path.join(topic_path, todo_file)
    with open(topic_todo_file, 'r') as f:
        return json.load(f)


def write_topic_todo(todo_json: str, topic: str) -> str:
    topic_path = os.path.join(todo_folder_path, topic)
    topic_todo_file = os.path.join(topic_path, todo_file)
    with open(topic_todo_file, 'w') as f:
        json.dump(todo_json, f)


def add_todo_to_topic(todo: str, topic: str) -> None:
    todo_json = load_topic(topic)
    todo_json["todos"].append(todo)
    write_topic_todo(todo_json, topic)


if __name__ == '__main__':
    cli()
