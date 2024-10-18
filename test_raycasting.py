import unittest
from your_main_game_file import lighting, walls, doomguy_pos, doomguy_vector, scale, fov

class TestRaycasting(unittest.TestCase):
     def test_ray_direction(self):
        expected_direction = (0, 1)
        doomguy_vector = math.pi / 2
        actual_direction = calculate_ray_direction(doomguy_vector, 0)
        self.assertEqual(actual_direction, expected_direction)

    def test_wall_collision(self):
        test_point = (2, 3)
        expected_collision = True
        actual_collision = check_wall_collision(test_point)
        self.assertEqual(actual_collision, expected_collision)

    def test_ray_length(self):
        expected_length = 5.0
        doomguy_pos = (0, 0)
        doomguy_vector = math.pi / 2 
        wall_position = (0, 5) 
        ray_length = calculate_ray_length(doomguy_pos, doomguy_vector, wall_position)  
        self.assertAlmostEqual(ray_length, expected_length, places=2)  
      
    def test_wall_hit_angle(self):
        expected_angle = math.pi / 4
        doomguy_pos = (0, 0)
        doomguy_vector = math.pi / 4
        wall_position = (1, 1)
        hit_angle = calculate_wall_hit_angle(doomguy_pos, doomguy_vector, wall_position)
        self.assertAlmostEqual(hit_angle, expected_angle, places=2) 
      
    def test_projected_height(self):
        expected_height = 100 
        ray_length = 5.0
        fov = math.pi / 3
        projected_height = calculate_projected_height(ray_length, fov)
        self.assertEqual(projected_height, expected_height)

    def test_lighting_color(self):
        expected_color = (255, 0, 0)
        ray_length = 10.0
        color = calculate_lighting_color(ray_length)
        self.assertEqual(color, expected_color)
