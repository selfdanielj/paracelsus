from paracelsus.graph import get_graph_string

from .utils import mermaid_assert


def test_get_graph_string(package_path):
    graph_string = get_graph_string(
        base_class_path="example.base:Base",
        import_module=["example.models"],
        include_tables=set(),
        exclude_tables=set(),
        python_dir=[package_path],
        format="mermaid",
    )
    mermaid_assert(graph_string)


def test_get_graph_string_with_exclude(package_path):
    """Excluding tables removes them from the graph string."""
    graph_string = get_graph_string(
        base_class_path="example.base:Base",
        import_module=["example.models"],
        include_tables=set(),
        exclude_tables={"comments"},
        python_dir=[package_path],
        format="mermaid",
    )
    assert "comments {" not in graph_string
    assert "posts {" in graph_string
    assert "users {" in graph_string
    assert "users ||--o{ posts" in graph_string

    # Excluding a table to which another table holds a foreign key will raise an error.
    graph_string = get_graph_string(
        base_class_path="example.base:Base",
        import_module=["example.models"],
        include_tables=set(),
        exclude_tables={"users", "comments"},
        python_dir=[package_path],
        format="mermaid",
    )
    assert "posts {" in graph_string
    assert "users ||--o{ posts" not in graph_string


def test_get_graph_string_with_include(package_path):
    """Excluding tables keeps them in the graph string."""
    graph_string = get_graph_string(
        base_class_path="example.base:Base",
        import_module=["example.models"],
        include_tables={"users", "posts"},
        exclude_tables=set(),
        python_dir=[package_path],
        format="mermaid",
    )
    assert "comments {" not in graph_string
    assert "posts {" in graph_string
    assert "users {" in graph_string
    assert "users ||--o{ posts" in graph_string

    # Including a table that holds a foreign key to a non-existing table will keep
    # the table but skip the connection.
    graph_string = get_graph_string(
        base_class_path="example.base:Base",
        import_module=["example.models"],
        include_tables={"posts"},
        exclude_tables=set(),
        python_dir=[package_path],
        format="mermaid",
    )
    assert "posts {" in graph_string
    assert "users ||--o{ posts" not in graph_string
