#!/usr/bin/env python3
"""Focused numerical checks for the generated cubemap GGX mip chain."""
import unittest
import struct
import tempfile
from pathlib import Path

import numpy as np

import tools.make_surface_maps as generator
from tools.make_surface_maps import (encode_cube, face_dirs, ggx_prefilter_mips,
                                     mark_cube_ini_irradiance, mark_cube_ini_prefiltered,
                                     sample_cube)


class GgxCubePrefilterTests(unittest.TestCase):
    def test_constant_environment_is_energy_preserving(self):
        faces = [np.full((8, 8, 3), 0.4, dtype=np.float32) for _ in range(6)]
        levels = ggx_prefilter_mips(faces, sample_count=16)

        self.assertEqual(len(levels), 6)
        self.assertEqual([len(face) for face in levels], [4] * 6)
        for face_id, face_levels in enumerate(levels):
            np.testing.assert_array_equal(face_levels[0], faces[face_id])
            for mip in face_levels[1:]:
                np.testing.assert_allclose(mip, 0.4, atol=2e-6)

    def test_rough_mips_blur_a_directional_highlight(self):
        faces = [np.zeros((16, 16, 3), dtype=np.float32) for _ in range(6)]
        faces[4][6:10, 6:10] = 1.0
        levels = ggx_prefilter_mips(faces, sample_count=64)

        self.assertEqual(levels[4][0].max(), 1.0)
        self.assertLess(float(levels[4][2].max()), 1.0)
        self.assertGreater(float(np.count_nonzero(levels[4][2] > 0.01)), 1)

    def test_rejects_incomplete_or_non_power_of_two_cubes(self):
        with self.assertRaises(ValueError):
            ggx_prefilter_mips([np.zeros((8, 8, 3), dtype=np.float32)] * 5)
        with self.assertRaises(ValueError):
            ggx_prefilter_mips([np.zeros((6, 6, 3), dtype=np.float32)] * 6)

    def test_direction_sampler_resolves_all_six_face_centers(self):
        colors = [np.full((8, 8, 3), i / 6, dtype=np.float32) for i in range(6)]
        directions = np.stack([face_dirs(8)[i][4, 4] for i in range(6)])
        samples = sample_cube(colors, directions)
        np.testing.assert_allclose(samples[:, 0], np.arange(6) / 6, atol=1e-6)

    def test_dds_contains_complete_prefiltered_mip_chain(self):
        faces = [np.full((8, 8, 3), 0.25, dtype=np.float32) for _ in range(6)]
        dds = encode_cube(faces, sample_count=16)
        self.assertEqual(struct.unpack_from("<I", dds, 28)[0], 4)
        expected = 128 + 6 * 4 * (8 * 8 + 4 * 4 + 2 * 2 + 1)
        self.assertEqual(len(dds), expected)

    def test_marks_only_requested_cubemap_sections_idempotently(self):
        text = ("[NormalMap]\ntexture = hull\n\n[CubeMap]\nnickname = sky\nfile = fx/sky.mat\n"
                "\n[CubeMap]\nnickname = legacy\nfile = fx/legacy.mat\n")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SurfaceMaps.ini"
            path.write_text(text, encoding="utf-8")
            mark_cube_ini_prefiltered(path, {"sky"})
            first = path.read_text(encoding="utf-8")
            mark_cube_ini_prefiltered(path, {"sky"})
            second = path.read_text(encoding="utf-8")
        self.assertEqual(first, second)
        self.assertEqual(first.count("prefiltered = true"), 1)
        self.assertIn("nickname = legacy\nfile = fx/legacy.mat\n", first)

    def test_marks_matching_irradiance_asset_idempotently(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SurfaceMaps.ini"
            path.write_text("[CubeMap]\nnickname = envcube_space\nfile = fx/envcube_space.mat\n\n"
                            "[CubeMap]\nnickname = envcube_sun\nfile = fx/envcube_sun.mat\n")
            mark_cube_ini_irradiance(path, {"envcube_space"})
            first = path.read_text()
            mark_cube_ini_irradiance(path, {"envcube_space"})
            self.assertEqual(first, path.read_text())
            self.assertIn("irradiance_file = fx\\envirradiance_space.mat", first)
            self.assertNotIn("envirradiance_sun", first)

    def test_diffuse_irradiance_preserves_constant_environment(self):
        color = np.array([0.3, 0.55, 0.8], dtype=np.float32)
        faces = [np.broadcast_to(color, (8, 8, 3)).copy() for _ in range(6)]
        result = generator.diffuse_irradiance_cube(faces, output_size=4, sample_count=64)
        expected = generator.linear_to_srgb(generator.srgb_to_linear(color))
        for face in result:
            self.assertTrue(np.allclose(face, expected[None, None, :], atol=1e-6))

    def test_diffuse_irradiance_is_directional_for_a_single_bright_face(self):
        faces = [np.zeros((8, 8, 3), dtype=np.float32) for _ in range(6)]
        faces[0][:] = 1.0
        result = generator.diffuse_irradiance_cube(faces, output_size=4, sample_count=128)
        self.assertGreater(float(result[0].mean()), float(result[1].mean()))


if __name__ == "__main__":
    unittest.main()
