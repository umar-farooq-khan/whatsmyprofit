from preprocessing import DataPreprocessing
from model import ClassificationModel


preproc = DataPreprocessing()
preproc.prepare_new_dataset()

model = ClassificationModel(preproc.input_shape)

train_x, train_y, val_x, val_y = preproc.get_data()

model.create_model()
model.train_model(train_x, train_y, val_x, val_y)

