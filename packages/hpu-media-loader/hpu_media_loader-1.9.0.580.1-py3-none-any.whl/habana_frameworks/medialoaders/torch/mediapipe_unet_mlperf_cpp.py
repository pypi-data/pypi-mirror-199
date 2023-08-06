#!/bin/env python
import numpy as np
import time
import glob
import matplotlib.pyplot as plt
from habana_frameworks.mediapipe.operators.cpu_nodes.cpu_nodes import media_function
from habana_frameworks.mediapipe import fn  # NOQA
from habana_frameworks.mediapipe.mediapipe import MediaPipe  # NOQA
from habana_frameworks.mediapipe.media_types import imgtype as it  # NOQA
from habana_frameworks.mediapipe.media_types import dtype as dt  # NOQA

flip_prob= 0.33
brightness_prob= 0.1
noise_prob= 0.1
class UnetMlPerfMediaPipe(MediaPipe):
    def __init__(self, device, queue_depth, batch_size, input_list, patch_size, seed, drop_remainder, num_slices, slice_index, num_threads=1, is_testing=False):
        super().__init__(device=device,
                         prefetch_depth=queue_depth,
                         batch_size=batch_size,
                         num_threads=num_threads,
                         pipe_name=self.__class__.__name__)
        if(seed == None):
            seed = int(time.time_ns() % (2**31 - 1))
        print("media data loader seed : ", seed)
        self.seed_mediapipe=seed
        self.set_aug_seed= int(time.time_ns() % (2**31 - 1))+1000
        self.batch_size = batch_size
        self.patch_size = patch_size.copy()
        self.pipe_drop_last=drop_remainder
        self.num_slices=num_slices
        self.slice_index=slice_index
        self.is_testing = is_testing

        self.pipe_reader_pad_remainder=False #??? How is it dependent of pipe_drop_last
        train_shuffle_across_dataset=True
        train_shuffle=True

        val_shuffle_across_dataset=True
        val_shuffle=True
        # reader
        if(self.is_testing==False):
            self.images = fn.ReadNumpyDatasetFromDir(num_outputs=1,
                                                    shuffle=train_shuffle,
                                                    shuffle_across_dataset=train_shuffle_across_dataset,
                                                    file_list=input_list[0],
                                                    dtype=dt.FLOAT32,
                                                    #dense=False,
                                                    seed=self.seed_mediapipe,
                                                    drop_remainder=self.pipe_drop_last,
                                                    pad_remainder=self.pipe_reader_pad_remainder,
                                                    num_slices=self.num_slices,
                                                    slice_index=self.slice_index,
                                                    device='cpu'
                                                    )
            
            self.labels = fn.ReadNumpyDatasetFromDir(num_outputs=1,
                                                    shuffle=train_shuffle,
                                                    shuffle_across_dataset=train_shuffle_across_dataset,
                                                    file_list=input_list[1],
                                                    dtype=dt.UINT8,
                                                    #dense=False,
                                                    seed=self.seed_mediapipe,
                                                    drop_remainder=self.pipe_drop_last,
                                                    pad_remainder=self.pipe_reader_pad_remainder,
                                                    num_slices=self.num_slices,
                                                    slice_index=self.slice_index,
                                                    device='cpu'
                                                    )

            # random biased crop
            self.rand_bias_crop = fn.RandomBiasedCrop(patch_size=patch_size,
                                            seed=self.set_aug_seed+10,
                                            cache_bboxes=True,
                                            dtype=[dt.FLOAT32, dt.UINT8, dt.UINT32], device='cpu')  # this output dtype is mandatory until cpp is generic

            # random flip
            self.random_flip_prob = fn.Constant(constant=flip_prob,dtype=dt.FLOAT32, device='cpu')
            self.flip_h = fn.CoinFlip(seed=self.set_aug_seed+335, device='cpu')
            self.flip_v = fn.CoinFlip(seed=self.set_aug_seed+253, device='cpu')
            self.flip_d = fn.CoinFlip(seed=self.set_aug_seed+173, device='cpu')

            self.img_hflip = fn.RandomFlip(horizontal=1, device='cpu')
            self.lbl_hflip = fn.RandomFlip(horizontal=1, device='cpu')
            self.img_vflip = fn.RandomFlip(vertical=1, device='cpu')
            self.lbl_vflip = fn.RandomFlip(vertical=1, device='cpu')
            self.img_dflip = fn.RandomFlip(depthwise=1, device='cpu')
            self.lbl_dflip = fn.RandomFlip(depthwise=1, device='cpu')

            # brightness
            self.brightness_probability = fn.Constant(constant=brightness_prob,dtype=dt.FLOAT32, device='cpu')
            self.coin_flip_b = fn.CoinFlip(seed=self.set_aug_seed+537, device='cpu')
            self.random_b = fn.RandomUniform(seed=self.set_aug_seed+698,
                                            low=0.7,
                                            high=1.3,
                                            device='cpu')
            self.const_b = fn.Constant(
                constant=1.0, dtype=dt.FLOAT32, device='cpu')
            self.where_b = fn.Where(device='cpu')
            self.brightness_op = fn.Mult(device='cpu')

            # gaussian noise
            self.gnoise_probability = fn.Constant(constant=noise_prob,dtype=dt.FLOAT32, device='cpu')
            self.coin_flip_g = fn.CoinFlip(seed=self.set_aug_seed+753,device='cpu')
            self.random_g = fn.RandomNormal(seed=self.set_aug_seed+995, mean=0, device='cpu')
            self.where_g = fn.Where(device='cpu')
            self.noise_op = fn.Add(device='cpu')
            self.const_std_dev_g = fn.Constant(
                constant=0.1, dtype=dt.FLOAT32, device='cpu')
            self.const_zero_g = fn.Constant(
                constant=0, dtype=dt.FLOAT32, device='cpu')
        else:
            self.val_images = fn.ReadNumpyDatasetFromDir(num_outputs=1,
                                                    shuffle=val_shuffle,
                                                    shuffle_across_dataset=val_shuffle_across_dataset,
                                                    file_list=input_list[0],
                                                    dtype=dt.FLOAT32,
                                                    #dense=False,
                                                    seed=self.seed_mediapipe,
                                                    drop_remainder=self.pipe_drop_last,
                                                    pad_remainder=self.pipe_reader_pad_remainder,
                                                    num_slices=self.num_slices,
                                                    slice_index=self.slice_index,
                                                    device='cpu'
                                                    )
            
            self.val_labels = fn.ReadNumpyDatasetFromDir(num_outputs=1,
                                                    shuffle=val_shuffle,
                                                    shuffle_across_dataset=val_shuffle_across_dataset,
                                                    file_list=input_list[1],
                                                    dtype=dt.UINT8,
                                                    #dense=False,
                                                    seed=self.seed_mediapipe,
                                                    drop_remainder=self.pipe_drop_last,
                                                    pad_remainder=self.pipe_reader_pad_remainder,
                                                    num_slices=self.num_slices,
                                                    slice_index=self.slice_index,
                                                    device='cpu'
                                                    )


    def definegraph(self):
        if(self.is_testing==False):
            img = self.images()
            lbl = self.labels()

            # biased crop
            img, lbl, coord = self.rand_bias_crop(img, lbl)
            
            # random flips
            rflip_prob = self.random_flip_prob()
            h_predicate = self.flip_h(rflip_prob)
            v_predicate = self.flip_v(rflip_prob)
            d_predicate = self.flip_d(rflip_prob)
            img = self.img_hflip(img, h_predicate)
            lbl = self.lbl_hflip(lbl, h_predicate)
            img = self.img_vflip(img, v_predicate)
            lbl = self.lbl_vflip(lbl, v_predicate)
            img = self.img_dflip(img, d_predicate)
            lbl = self.lbl_dflip(lbl, d_predicate)

            # brightness
            b_prob=self.brightness_probability()
            scale = self.random_b()
            b_predicate = self.coin_flip_b(b_prob)
            scale_def = self.const_b()#1.0
            scale = self.where_b(b_predicate, scale, scale_def)
            #scale = self.where_b(b_predicate, scale_def, scale)
            img = self.brightness_op(img, scale)

            # gaussian noise

            gn_prob=self.gnoise_probability()
            g_predicate = self.coin_flip_g(gn_prob)
            std_dev_in = self.const_std_dev_g() #0.1
            std_dev_def = self.const_zero_g() #0
            std_dev = self.where_g(g_predicate, std_dev_in, std_dev_def)
            noiseVal = self.random_g(std_dev, img)
            img = self.noise_op(img, noiseVal)

            return img, lbl
        else:
            img = self.val_images()
            lbl = self.val_labels()
            return img, lbl

"""def main_multi_pipe():
    seed = int(time.time_ns() % (2**31 - 1))
    epochs = 1
    is_testing = False
    batch_size = 1
    queue_depth = 3
    drop_remainder = True
    patch_size = [128, 128, 128]
    dir = "/software/data/unet3d/kits19/preprocessed_data/"
    pattern0 = "case_*_x.npy"
    pattern1 = "case_*_y.npy"
    x_in = np.array(sorted(glob.glob(dir + "/{}".format(pattern0))))
    y_in = np.array(sorted(glob.glob(dir + "/{}".format(pattern1))))
    input_list = [x_in, y_in]
    ##################### pipe_1 ######################
    pipe1 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=0,
                               is_testing=is_testing)
 
    pipe1.build()

    ################### pipe_2 #######################
    pipe2 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=1,
                               is_testing=is_testing)
 
    pipe2.build()

    ##################### pipe_3 ######################
    pipe3 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=2,
                               is_testing=is_testing)
 
    pipe3.build()

    ##################### pipe_4 ######################
    pipe4 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=3,
                               is_testing=is_testing)
 
    pipe4.build()

    ##################### pipe_5 ######################
    pipe5 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=4,
                               is_testing=is_testing)
 
    pipe5.build()

    ##################### pipe_6 ######################
    pipe6 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=5,
                               is_testing=is_testing)
 
    pipe6.build()

    ##################### pipe_7 ######################
    pipe7 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=6,
                               is_testing=is_testing)
 
    pipe7.build()

    ##################### pipe_8 ######################
    pipe8 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=7,
                               is_testing=is_testing)
 
    pipe8.build()

    epochs=100
    for i in range(epochs):
        pipe1.iter_init()
        pipe2.iter_init()
        pipe3.iter_init()
        pipe4.iter_init()
        pipe5.iter_init()
        pipe6.iter_init()
        pipe7.iter_init()
        pipe8.iter_init()
        bcnt = 0
        while(1):#while(bcnt<2):
            try:
                print("Running epoch:",i," batch:",bcnt)
                img1, lbl1 = pipe1.run()
                img1 = img1.as_nparray()
                lbl1 = lbl1.as_nparray()
                print('cpu shape', img1.shape, lbl1.shape)

                img2, lbl2 = pipe2.run()
                img2 = img2.as_nparray()
                lbl2 = lbl2.as_nparray()
                print('cpu shape', img2.shape, lbl2.shape)

                img3, lbl3 = pipe3.run()
                img3 = img3.as_nparray()
                lbl3 = lbl3.as_nparray()
                print('cpu shape', img3.shape, lbl3.shape)

                img4, lbl4 = pipe4.run()
                img4 = img4.as_nparray()
                lbl4 = lbl4.as_nparray()
                print('cpu shape', img4.shape, lbl4.shape)

                img5, lbl5 = pipe5.run()
                img5 = img5.as_nparray()
                lbl5 = lbl5.as_nparray()
                print('cpu shape', img5.shape, lbl5.shape)

                img6, lbl6 = pipe6.run()
                img6 = img6.as_nparray()
                lbl6 = lbl6.as_nparray()
                print('cpu shape', img6.shape, lbl6.shape)

                img7, lbl7 = pipe7.run()
                img7 = img7.as_nparray()
                lbl7 = lbl7.as_nparray()
                print('cpu shape', img7.shape, lbl7.shape)

                img8, lbl8 = pipe8.run()
                img8 = img8.as_nparray()
                lbl8 = lbl8.as_nparray()
                print('cpu shape', img8.shape, lbl8.shape)
                
                bcnt = bcnt + 1
            except StopIteration:
                break
            del img1
            del lbl1
            del img2
            del lbl2
            del img3
            del lbl3
            del img4
            del lbl4
            del img5
            del lbl5
            del img6
            del lbl6
            del img7
            del lbl7
            del img8
            del lbl8
    del pipe1
    del pipe2
    del pipe3
    del pipe4
    del pipe5
    del pipe6
    del pipe7
    del pipe8"""


def main():
    seed = int(time.time_ns() % (2**31 - 1))
    epochs = 1
    is_testing = False
    batch_size = 1
    queue_depth = 3
    drop_remainder = True
    patch_size = [128, 128, 128]
    dir = "/software/data/unet3d/kits19/preprocessed_data/"
    pattern0 = "case_*_x.npy"
    pattern1 = "case_*_y.npy"
    x_in = np.array(sorted(glob.glob(dir + "/{}".format(pattern0))))
    y_in = np.array(sorted(glob.glob(dir + "/{}".format(pattern1))))
    input_list = [x_in, y_in]
    ##################### pipe_1 ######################
    pipe1 = UnetMlPerfMediaPipe(device='cpu',
                               queue_depth=queue_depth,
                               batch_size=batch_size,
                               input_list=input_list,
                               patch_size=patch_size,
                               seed=seed,
                               drop_remainder=drop_remainder,
                               num_slices=8,
                               slice_index=0,
                               is_testing=is_testing)
 
    pipe1.build()

    epochs=100
    for i in range(epochs):
        pipe1.iter_init()
        bcnt = 0
        while(1):#while(bcnt<2):
            try:
                print("Running epoch:",i," batch:",bcnt)
                img1, lbl1 = pipe1.run()
                img1 = img1.as_nparray()
                lbl1 = lbl1.as_nparray()
                print('cpu shape', img1.shape, lbl1.shape)                
                bcnt = bcnt + 1
            except StopIteration:
                break
            del img1
    del pipe1

if __name__ == "__main__":
    main()
