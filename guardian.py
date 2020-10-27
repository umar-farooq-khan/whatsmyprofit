
from theguardian import theguardian_tag

header = {
        "q": "apple",
        "section": "technology",
    }
t = theguardian_tag.Tag(api="test", **header)
print(t.get_references_in_page(1))