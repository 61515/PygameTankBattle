class Coordinate:
    @staticmethod
    def xy_to_left_top_pixel(row_num, col_num):
        return col_num * 32, row_num * 32
