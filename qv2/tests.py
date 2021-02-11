import os.path
import unittest

import numpy as np

import qv2


class TestCase(unittest.TestCase):
    """
    Base class for test cases.
    """
    
    def assertNumpyShape(self, image, shape):
        self.assertIsInstance(image, np.ndarray)
        self.assertEqual(image.shape, shape)
    
    def assertIsImage(self, x):
        self.assertTrue(qv2.is_image(image=x))
    
    def assertEqualImageContainers(self, x, y):
        self.assertIsImage(x)
        self.assertIsImage(y)
        self.assertEqual(x.dtype, y.dtype)
        self.assertEqual(x.shape, y.shape)
    
    def assertEqualImages(self, x, y):
        self.assertEqualImageContainers(x, y)
        self.assertTrue(np.all(x == y))
        

class dtype_range_Tests(TestCase):
    def test_dtype_range_uint8(self):
        range_ = qv2.dtype_range(dtype=np.uint8)
        self.assertEqual(range_, (0, 2**8 - 1))
        
    def test_dtype_range_uint16(self):
        range_ = qv2.dtype_range(dtype=np.uint16)
        self.assertEqual(range_, (0, 2**16 - 1))
    
    def test_dtype_range_uint32(self):
        range_ = qv2.dtype_range(dtype=np.uint32)
        self.assertEqual(range_, (0, 2**32 - 1))
    
    def test_dtype_range_int8(self):
        range_ = qv2.dtype_range(dtype=np.int8)
        self.assertEqual(range_, (-2**7, 2**7 - 1))
    
    def test_dtype_range_int16(self):
        range_ = qv2.dtype_range(dtype=np.int16)
        self.assertEqual(range_, (-2**15, 2**15 - 1))
    
    def test_dtype_range_int32(self):
        range_ = qv2.dtype_range(dtype=np.int32)
        self.assertEqual(range_, (-2**31, 2**31 - 1))
    
    def test_dtype_range_float32(self):
        range_ = qv2.dtype_range(dtype=np.float32)
        self.assertEqual(range_, (0, 1.0))
        
    def test_dtype_range_float64(self):
        range_ = qv2.dtype_range(dtype=np.float64)
        self.assertEqual(range_, (0, 1.0))
        
    def test_dtype_range_bool(self):
        range_ = qv2.dtype_range(dtype=np.bool_)
        self.assertEqual(range_, (False, True))


####
#%%% TODO: refactor
####


class aliases_Tests(TestCase):
    def test_otsu_raise(self):
        image = qv2.pm5544()
        self.assertRaises(ValueError, lambda: qv2.otsu(image=image))
        
    def test_otsu_return(self):
        image = qv2.pm5544()
        image_gray = qv2.as_gray(image)
        result = qv2.otsu(image=image_gray)
        self.assertIsInstance(result, tuple)
        self.assertTrue(len(result) == 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], np.ndarray)
    
    def test_otsu_theta(self):
        image = qv2.pm5544()
        image_gray = qv2.as_gray(image)
        theta = qv2.otsu_theta(image=image_gray)
        self.assertIsInstance(theta, float)
        self.assertAlmostEqual(theta, 89.0)


class core_Tests(TestCase):
    def test_is_gray(self):
        image = qv2.pm5544()
        self.assertFalse(qv2.is_gray(image))
        self.assertTrue(qv2.is_gray(image[:, :, 0]))
        self.assertTrue(qv2.is_gray(image[:, :, 0:1]))
        self.assertFalse(qv2.is_gray(image[:, :, 0:2]))
    
    def test_is_color(self):
        image = qv2.pm5544()
        self.assertTrue(qv2.is_color(image))
        self.assertFalse(qv2.is_color(image[:, :, 0]))
        self.assertFalse(qv2.is_color(image[:, :, 0:1]))
        self.assertFalse(qv2.is_color(image[:, :, 0:2]))
    
    def test_as_gray(self):
        image = qv2.pm5544()
        self.assertTrue(qv2.is_color(image))
        image_g = qv2.as_gray(image)
        self.assertTrue(qv2.is_gray(image_g))
        self.assertEqual(image_g.shape, image.shape[:2])
    
    def test_as_gray_noop(self):
        image = qv2.pm5544()
        image_b = image[:, :, 0]
        self.assertEqualImages(image_b, qv2.as_gray(image_b))
        
    def test_as_color(self):
        image = qv2.pm5544()
        image_b = image[:, :, 0]
        image_c = qv2.as_color(image_b)
        self.assertTrue(qv2.is_color(image_c))
        self.assertEqual(image_c.shape, image_b.shape + (3,))
        for n_channel in range(3):
            self.assertEqualImages(image_c[:, :, n_channel], image_b)
    
    def test_as_color_noop(self):
        image = qv2.pm5544()
        self.assertEqualImages(image, qv2.as_color(image))
    
    def test_flip_channels_values(self):
        image = qv2.pm5544()
        image_flipped = qv2.flip_channels(image=image)
        for n_channel in range(3):
            self.assertEqualImages(image[:, :, n_channel], image_flipped[:, :, 2 - n_channel])
        
    def test_flip_channels_once_neq(self):
        image = qv2.pm5544()
        image_flipped = qv2.flip_channels(image=image)
        self.assertEqualImageContainers(image, image_flipped)
        self.assertFalse(np.all(image == image_flipped))
        
    def test_flip_channels_twice(self):
        image = qv2.pm5544()
        image_flipped = qv2.flip_channels(image=image)
        image_flipped_flipped = qv2.flip_channels(image=image_flipped)
        self.assertEqualImages(image, image_flipped_flipped)


class data_Tests(TestCase):
    def test_data_dir_exists(self):
        self.assertTrue(os.path.exists(qv2.DATA_DIR))
    
    def test_data_files_exists(self):
        for filename in qv2.DATA_FILENAMES.values():
            self.assertTrue(os.path.exists(filename), "Data file '{}' does not exist".format(filename))
    
    def test_colormap_plot(self):
        result = qv2.colormap("plot")
        self.assertTrue(qv2.is_colormap(result))
        self.assertEqual(result[0, 0, :].tolist(), [0, 0, 0])
        self.assertEqual(result[1, 0, :].tolist(), [0, 0, 255])
        self.assertEqual(result[2, 0, :].tolist(), [0, 255, 0])
        self.assertEqual(result[3, 0, :].tolist(), [255, 0, 0])
        self.assertEqual(result[255, 0, :].tolist(), [255, 255, 255])

    def test_colormap_jet(self):
        result = qv2.colormap("jet")
        self.assertTrue(qv2.is_colormap(result))
        
    def test_colormap_raise(self):
        self.assertRaises(ValueError, lambda: qv2.colormap("__!?-non-existing_colormap-name-!?__"))
    
    def test_pm5544_load(self):
        image = qv2.pm5544()
        self.assertIsImage(image)
        self.assertEqual(image.shape, (576, 768, 3))
    
    def test_xslope_width256(self):
        for height in (1, 32):
            slope = qv2.xslope(height=height, width=256)
            self.assertIsImage(slope)
            self.assertEqual(slope.dtype, np.uint8)
            self.assertEqual(slope.shape, (height, 256))
            for x in range(256):
                for y in range(height):
                    self.assertEqual(slope[y, x], x)
    
    def test_xslope_widthNot256(self):
        height = 1
        for width in (2, 32, 256, 1000):
            slope = qv2.xslope(height=height, width=width)
            self.assertIsImage(slope)
            self.assertEqual(slope.dtype, np.uint8)
            self.assertEqual(slope.shape, (height, width))
            for y in range(height):
                self.assertEqual(slope[y, 0], 0)
                self.assertEqual(slope[y, width - 1], 255)

    def test_yslope(self):
        height = 256
        width = 32
        slope = qv2.yslope(width=width, height=height)
        self.assertIsImage(slope)
        self.assertEqual(slope.dtype, np.uint8)
        self.assertEqual(slope.shape, (height, width))
        for x in range(width):
            for y in range(height):
                self.assertEqual(slope[y, x], y)


class geometry_Tests(TestCase):
    def test_size(self):
        image = qv2.pm5544()
        self.assertEqual(qv2.size(image), (768, 576))

    def test_resize_scale(self):
        image = qv2.pm5544()
        image2 = qv2.resize(image, 0.5)
        self.assertEqual(image2.shape, (288, 384, 3))
        
    def test_resize_size(self):
        image = qv2.pm5544()
        image2 = qv2.resize(image, (384, 288))
        self.assertEqual(image2.shape, (288, 384, 3))


class infos_Tests(TestCase):
    def test_info(self):
        image = qv2.pm5544()
        info = qv2.info(image)
        self.assertEqual(info["shape"], (576, 768, 3))
        self.assertAlmostEqual(info["mean"], 121.3680261682581)
        self.assertAlmostEqual(info["std"], 91.194048489528782)
        self.assertEqual(info["min"], 0)
        self.assertAlmostEqual(info["3rd quartile"], 191.0)
        self.assertEqual(info["max"], 255)
        
    def test_hist_color(self):
        image = qv2.pm5544()
        h = qv2.hist(image, bin_count=256)
        self.assertAlmostEqual(h[0], 328389.0)
        self.assertAlmostEqual(h[6], 1512.0)
        self.assertAlmostEqual(h[86], 0.0)
        self.assertAlmostEqual(h[122], 330802.0)
        self.assertAlmostEqual(h[134], 7.0)
        self.assertAlmostEqual(h[191], 112044.0)
        self.assertAlmostEqual(h[195], 3.0)
        self.assertAlmostEqual(h[255], 212526.0)
        
    def test_hist_gray(self):
        image = qv2.pm5544()
        image_b = image[:, :, 0]
        h = qv2.hist(image_b, bin_count=256)
        self.assertAlmostEqual(h[11], 18036.0)
        self.assertAlmostEqual(h[73], 88.0)
        self.assertAlmostEqual(h[170], 2528.0)
        self.assertAlmostEqual(h[255], 70842.0)
    
    def test_hist_gray_2dim_vs_3dim(self):
        image = qv2.pm5544()
        
        image_2dim = image[:, :, 0]
        h_2dim = qv2.hist(image_2dim, bin_count=256)
        
        image_3dim = image_2dim.copy()
        image_3dim.shape = image_3dim.shape + (1,)
        h_3dim = qv2.hist(image_3dim, bin_count=256)
        
        self.assertEqual(len(h_2dim), len(h_3dim))
        for (value_2dim, value_3dim) in zip(h_2dim, h_3dim):
            self.assertAlmostEqual(value_2dim, value_3dim)
            
    def test_hist_gray_vs_color(self):
        image = qv2.pm5544()
        
        image_b = image[:, :, 0]
        image_g = image[:, :, 1]
        image_r = image[:, :, 2]

        h_sum = qv2.hist(image_b, bin_count=256) + qv2.hist(image_g, bin_count=256) + qv2.hist(image_r, bin_count=256)
        h_color = qv2.hist(image, bin_count=256)
        
        self.assertEqual(len(h_sum), len(h_color))
        for (value_sum, value_color) in zip(h_sum, h_color):
            self.assertAlmostEqual(value_sum, value_color)


class io_Tests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_filename = os.path.join(qv2.DATA_FILENAMES["image:PM5544"])
        self.shape = (576, 768, 3)
    
    def test_load_default(self):
        image = qv2.load(filename=self.image_filename)
        self.assertNumpyShape(image, self.shape)
        self.assertAlmostEqual(np.mean(image), 121.3680261682581)
        
    def test_load_grayscale(self):
        image = qv2.load(filename=self.image_filename, color=False)
        self.assertNumpyShape(image, self.shape[:2])
        
    def test_decode_default(self):
        with open(self.image_filename, "rb") as f:
            image = qv2.decode(b=f.read())
        self.assertNumpyShape(image, self.shape)
        self.assertAlmostEqual(np.mean(image), 121.3680261682581)
        
    def test_decode_grayscale(self):
        with open(self.image_filename, "rb") as f:
            image = qv2.decode(b=f.read(), color=False)
        self.assertNumpyShape(image, self.shape[:2])
        
    def test_load_and_decode_equal(self):
        image_load = qv2.load(filename=self.image_filename)
        with open(self.image_filename, "rb") as f:
            image_decode = qv2.decode(b=f.read())
        self.assertNumpyShape(image_load, self.shape)    
        self.assertNumpyShape(image_decode, self.shape)
        self.assertTrue(np.all(image_load == image_decode))


class transforms_Tests(TestCase):
    pass

        
class utils_Tests(TestCase):
    def test_tir_args(self):
        items = (1.24, -1.87)
        self.assertEqual(qv2.tir(*items), (1, -2))
        self.assertEqual(qv2.tir(items), (1, -2))
        self.assertEqual(qv2.tir(list(items)), (1, -2))

        
if __name__ == "__main__":
    unittest.main()