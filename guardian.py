import os
import cv2
import shutil
import numpy as np
import imutils
# from skimage.io import imread     # pip install scikit-image
# from skimage.transform import resize
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as k
from keras.preprocessing import image
from tensorflow.keras.applications import ResNet50

from keras.applications import VGG19


class DataPreprocessing:

    def __init__(self):
        self.img_width, self.img_height = 200, 200
        self.input_shape = (self.img_width, self.img_height, 3)
        self.cats = ['N', 'M', 'B']
        self.batch_size = 20
        self.train_data_dir = "tf/data/training/"
        self.validation_data_dir = 'tf/data/validation/'

    def get_data(self):
        empty_arr = np.array([])
        train_x_side, train_x_top, train_y, val_x_side, val_x_top, val_y = empty_arr, empty_arr, empty_arr, empty_arr, empty_arr, empty_arr

        for cat in self.cats:
            side_imgs, top_imgs, y_cats = self.get_img_lst(
                self.train_data_dir.replace('tf/data/', 'tf/data_processed/'),
                cat)

            if (train_x_side.shape == (0,)):
                train_x_side = side_imgs
            else:
                train_x_side = np.concatenate((train_x_side, side_imgs), axis=0)

            if (train_x_top.shape == (0,)):
                train_x_top = top_imgs
            else:
                train_x_top = np.concatenate((train_x_top, top_imgs), axis=0)

            if (train_y.shape == (0,)):
                train_y = y_cats
            else:
                train_y = np.concatenate((train_y, y_cats), axis=0)

        for cat in self.cats:
            side_imgs, top_imgs, y_cats = self.get_img_lst(
                self.validation_data_dir.replace('tf/data/', 'tf/data_processed/'), cat)

            if (val_x_side.shape == (0,)):
                val_x_side = side_imgs
            else:
                val_x_side = np.concatenate((val_x_side, side_imgs), axis=0)

            if (val_x_top.shape == (0,)):
                val_x_top = top_imgs

            else:
                val_x_top = np.concatenate((val_x_top, top_imgs), axis=0)

            if (val_y.shape == (0,)):
                val_y = y_cats
            else:
                val_y = np.concatenate((val_y, y_cats), axis=0)

        print('train_x_side', train_x_side.shape, 'train_y', train_y.shape)
        print('val_x_side', val_x_side.shape, 'val_y', val_y.shape)

        return [train_x_side, train_x_top], train_y, [val_x_side, val_x_top], val_y

    def get_img_lst(self, dir, cat):
        side_imgs, top_imgs = [], []
        y_cats = []

        for side_pth in os.listdir(dir + cat + '/mlo/'):

            side_pth = os.path.join(dir, cat + '/mlo/' + side_pth)
            top_pth = side_pth.replace('/mlo/', '/cc/')

            try:
                side_img = cv2.imread(side_pth)
                top_img = cv2.imread(top_pth)

                side_imgs.append(side_img)
                top_imgs.append(top_img)

                y_cats.append(self.cats.index(cat))

            except:
                print("can't find " + str(top_pth))

        side_imgs = np.array(side_imgs)
        top_imgs = np.array(top_imgs)
        y_cats = to_categorical(np.array(y_cats), 3)
        # print(y_cats, y_cats.shape)

        side_imgs = side_imgs / 255.0
        top_imgs = top_imgs / 255.0

        # side_imgs.reshape(side_imgs.shape[0], self.input_shape[0], self.input_shape[1], 1)
        # top_imgs.reshape(top_imgs.shape[0], self.input_shape[0], self.input_shape[1], 1)

        return side_imgs, top_imgs, y_cats

    def prepare_new_dataset(self):
        print('Preparing dataset ...')
        main_new_dir = "tf/data_processed/"
        main_dir = "tf/data/"

        if os.path.exists(main_new_dir):
            shutil.rmtree(main_new_dir)

        os.makedirs(main_new_dir)

        for sub_dir in ["training/", "validation/"]:
            if not os.path.exists(main_new_dir + sub_dir):
                os.makedirs(main_new_dir + sub_dir)

            for cat_ in self.cats:
                if not os.path.exists(main_new_dir + sub_dir + cat_):
                    os.makedirs(main_new_dir + sub_dir + cat_)
                    os.makedirs(main_new_dir + sub_dir + cat_ + '/mlo/')
                    os.makedirs(main_new_dir + sub_dir + cat_ + '/cc/')

                    for side_pth in os.listdir(main_dir + sub_dir + cat_ + '/mlo/'):

                        side_pth = main_dir + sub_dir + cat_ + '/mlo/' + side_pth
                        top_pth = side_pth.replace('/mlo/', '/cc/')

                        try:
                            side_img = cv2.imread(side_pth)
                            side_img_new = self.crop_img(side_img)
                            side_img_new = cv2.resize(side_img_new, (self.img_width, self.img_height),
                                                      interpolation=cv2.INTER_AREA)
                            cv2.imwrite(side_pth.replace('tf/data/', 'tf/data_processed/'), side_img_new)

                            top_img = cv2.imread(top_pth)
                            top_img_new = self.crop_img(top_img)
                            top_img_new = cv2.resize(top_img_new, (self.img_width, self.img_height),
                                                     interpolation=cv2.INTER_AREA)
                            cv2.imwrite(top_pth.replace('tf/data/', 'tf/data_processed/'), top_img_new)

                        except:
                            print("can't find " + str(top_pth))

    def crop_img(self, img, add_pixels_value=0):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        ADD_PIXELS = add_pixels_value
        new_img = img[extTop[1] - ADD_PIXELS:extBot[1] + ADD_PIXELS,
                  extLeft[0] - ADD_PIXELS:extRight[0] + ADD_PIXELS].copy()

        return new_img


from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras import optimizers, losses, activations, models
from keras.layers import Conv2D, MaxPooling2D, concatenate
from keras.layers import Activation, Dropout, Flatten, Dense, Input
from keras.models import Model
from keras import backend as k
from keras import applications
import numpy as np
from keras.preprocessing import image
from tensorflow.keras.applications import ResNet50
from keras.applications import VGG19


class ClassificationModel:

    def __init__(self, input_shape):
        self.input_shape = input_shape
        self.epochs = 100
        self.num_classes = 3

    def create_model(self):
        side_view_input = Input(shape=self.input_shape)
        side_view_model = self.create_convolution_layers(side_view_input)

        # base_model =VGG19(weights='imagenet', include_top=False,input_shape=self.input_shape)
        # for layer in base_model.layers:
        #     layer.trainable = False
        # # add_model = Sequential()
        # add_model= base_model.output
        # add_model= Flatten() (add_model)
        # add_model= Dropout(0.2) (add_model)
        # add_model= Dense(1024, activation='relu') (add_model)
        # add_model= Dropout(0.3) (add_model)
        # add_model= Dense(1024, activation='relu') (add_model)

        # side_view_model = add_model

        top_view_input = Input(shape=self.input_shape)
        top_view_model = self.create_convolution_layers(top_view_input)

        # base_model2 =VGG19(weights='imagenet', include_top=False,input_shape=self.input_shape)
        # # add_model2 = Sequential()
        # add_model2= base_model2.output()
        # add_model2= Flatten() (add_model2)
        # add_model2= Dropout(0.2) (add_model2)
        # add_model2= Dense(1024, activation='relu') (add_model2)
        # add_model2= Dropout(0.3) (add_model2)
        # add_model2= Dense(1024, activation='relu') (add_model2)
        # top_view_model = add_model2

        conc_model = concatenate([side_view_model, top_view_model])
        conc_model = Flatten()(conc_model)
        conc_model = Dense(512)(conc_model)
        # conc_model = Dense(128)(conc_model)
        conc_model = Activation('relu')(conc_model)
        conc_model = Dropout(0.5)(conc_model)

        conc_model = Dense(self.num_classes, activation='softmax')(conc_model)

        model = Model(inputs=[side_view_input, top_view_input], outputs=[conc_model])

        model.compile(loss='categorical_crossentropy',
                      optimizer=optimizers.Adam(),
                      metrics=['accuracy'])
        model.summary()

        self.model = model

    def create_convolution_layers(self, input_img):
        # model = Conv2D(32, (3, 3), padding='same', input_shape=self.input_shape)(input_img)
        # model = Activation('relu')(model)
        # model = MaxPooling2D((2, 2), padding='same')(model)

        # model = Conv2D(256, (3, 3), padding='same')(model)
        # model = Activation('relu')(model)
        # model = MaxPooling2D(pool_size=(2, 2), padding='same')(model)
        # model = Dropout(0.2)(model)
        # model = Conv2D(128, (3, 3), padding='same')(model)
        # model = Activation('relu')(model)
        # model = MaxPooling2D(pool_size=(2, 2), padding='same')(model)
        # model = Dropout(0.4)(model)
        # model = Conv2D(32, kernel_size=5)(input_img)
        # model = Activation('relu')(model)
        # model = MaxPooling2D(pool_size=(2,2))(model)
        # model = Flatten()(model)

        base_model = VGG19(weights='imagenet',
                           include_top=False,
                           input_shape=self.input_shape)(input_img)

        for layer in base_model.layers:
            layer.trainable = False

        y = base_model
        y = Flatten()(y)
        y = Dropout(0.2)(y)
        y = Dense(1024, activation='relu')(y)
        y = Dropout(0.3)(y)
        y = Dense(1024, activation='relu')(y)
        return y

    def train_model(self, train_x, train_y, validation_x, validation_y):
        self.model.fit(
            train_x,
            train_y,
            epochs=self.epochs,
            validation_data=(validation_x, validation_y)
        )

        self.model.save_weights('yy4.h5')


preproc = DataPreprocessing()
preproc.prepare_new_dataset()

model = ClassificationModel(preproc.input_shape)

train_x, train_y, val_x, val_y = preproc.get_data()

model.create_model()
model.train_model(train_x, train_y, val_x, val_y)


