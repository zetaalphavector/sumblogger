a = [
    {
        "first_batch_summary": [
            "This is the summary for document 0",
            "This is the summary for document 1",
        ],
        "document": ["This is document 0", "This is document 1"],
    },
    {
        "second_batch_summary": [
            "This is the summary for document 0",
            "This is the summary for document 1",
        ],
        "document": ["This is document 0", "This is document 1"],
    },
]

merged = {
    "first_batch_summary": [
        ["This is the summary for document 0", "This is the summary for document 1"]
    ],
    "document": [
        ["This is document 0", "This is document 1"],
        ["This is document 0", "This is document 1"],
    ],
    "second_batch_summary": [
        ["This is the summary for document 0", "This is the summary for document 1"]
    ],
}
