from ragatouille import RAGTrainer

my_data = [
    ("What is the meaning of life ?", "The meaning of life is 42"),
    ("What is Neural Search?", "Neural Search is a terms referring to a family of ..."),
    ...
]  # Unlabelled pairs here

trainer = RAGTrainer()
trainer.prepare_training_data(raw_data=my_data)