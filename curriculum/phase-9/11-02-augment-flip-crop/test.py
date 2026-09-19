import random
import unittest
from collections import Counter

from solution import augment_flip_crop

IMG = [[r * 10 + c for c in range(5)] for r in range(4)]  # 4 rows x 5 cols, all pixels distinct


def windows(img, k):
    h, w = len(img), len(img[0])
    return [[row[l:l + k] for row in img[t:t + k]] for t in range(h - k + 1) for l in range(w - k + 1)]


class TestAugmentFlipCrop(unittest.TestCase):
    def test_output_shape(self):
        out = augment_flip_crop(IMG, random.Random(0), 3)
        self.assertEqual(len(out), 3)
        self.assertTrue(all(len(row) == 3 for row in out))

    def test_matches_the_specified_draws(self):
        for seed in range(20):
            d = random.Random(seed)
            flip = d.random() < 0.5
            top, left = d.randint(0, 4 - 2), d.randint(0, 5 - 2)
            src = [row[::-1] for row in IMG] if flip else IMG
            want = [row[left:left + 2] for row in src[top:top + 2]]
            self.assertEqual(augment_flip_crop(IMG, random.Random(seed), 2), want, msg=f"seed {seed}")

    def test_output_is_a_window_of_the_image_or_its_mirror(self):
        mirror = [row[::-1] for row in IMG]
        allowed = windows(IMG, 3) + windows(mirror, 3)
        for seed in range(50):
            self.assertIn(augment_flip_crop(IMG, random.Random(seed), 3), allowed)

    def test_pixels_come_from_the_input(self):
        pool = Counter(v for row in IMG for v in row)
        for seed in range(30):
            got = Counter(v for row in augment_flip_crop(IMG, random.Random(seed), 2) for v in row)
            self.assertEqual(got - pool, Counter())

    def test_both_flipped_and_unflipped_occur(self):
        full = [augment_flip_crop(IMG[:4], random.Random(s), 4) for s in range(40)]
        # crop 4 on a 4x5 image: the first row starts with 0 unless flipped
        firsts = {out[0][0] for out in full}
        self.assertTrue(any(v in (0, 1) for v in firsts))
        self.assertTrue(any(v in (4, 3) for v in firsts))

    def test_full_size_crop_returns_whole_image(self):
        sq = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        mirror = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
        seen = {str(augment_flip_crop(sq, random.Random(s), 3)) for s in range(30)}
        self.assertEqual(seen, {str(sq), str(mirror)})

    def test_does_not_mutate_input(self):
        img = [[1, 2], [3, 4]]
        for s in range(10):
            augment_flip_crop(img, random.Random(s), 1)
        self.assertEqual(img, [[1, 2], [3, 4]])

    def test_rejects_bad_crop(self):
        for crop in (0, 5, 6):
            with self.assertRaises(ValueError):
                augment_flip_crop(IMG, random.Random(0), crop)


if __name__ == "__main__":
    unittest.main(verbosity=2)
