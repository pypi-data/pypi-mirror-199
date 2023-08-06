# Input Module
class UI:
    @staticmethod
    def keyboard(prompt):
        response = input(f'{prompt}\n')
        return response
