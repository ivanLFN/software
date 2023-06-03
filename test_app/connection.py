import serial
import random

class ConnectionAruino():
    def __init__(self, main_window) -> None:
        self.main_window = main_window

        # Инициализация начальных значений
        self.default_settings()

        # Список кортежев с значениями
        self.data = []
        
    

    def default_settings(self):

        self.com = "COM3"
        self.name = "9600"

        # Настройки мотора X
        self.x_step = 2
        self.x_direct = 5

        # Настройки мотора Y
        self.y_step = 3
        self.y_direct = 6

        # Настройки мотора Z
        self.z_step = 4
        self.z_direct = 7

    def set_settings(self):
        
        self.com = self.main_window.ui.COM.currentText()
        self.name = self.main_window.ui.name.text()

        # Настройки мотора X
        self.x_step = self.main_window.ui.x_step.text()
        self.x_direct = self.main_window.ui.x_direct.text()

        # Настройки мотора Y
        self.y_step = self.main_window.ui.y_step.text()
        self.y_direct = self.main_window.ui.y_direct.text()

        # Настройки мотора Z
        self.z_step = self.main_window.ui.z_step.text()
        self.z_direct = self.main_window.ui.z_direct.text()

    def check_connection(self):
        try:
            ser = serial.Serial(self.com)
            ser.close()
            
            self.main_window.pritn_to_console(f'The connection to the {self.com} port has been established [OK]')
            return f"Подключение к порту {self.com} установлено."
            
        except serial.SerialException:
            self.main_window.pritn_to_console(f'Failed to connect to port {self.com} : {serial.SerialException} [ERR]')
            return f"Не удалось подключиться к порту {self.com}."
        
    def rotate_axle(self, axle, step_count, dir):

        command = b'r'

        self.arduino = serial.Serial(self.com, self.name)
        
        if axle == 'x':
            pin1 = self.x_step
            pin2 = self.x_direct
        if axle == 'y':
            pin1 = self.y_step
            pin2 = self.y_direct
        else:
            pin1 = self.z_step
            pin2 = self.z_direct

        self.arduino.write(command.encode())
        self.arduino.write(bytes([pin1, pin2]))
        self.arduino.write(str(step_count).encode())
        self.arduino.write(str(dir).encode())

    def get_data(self):

        # Получение данных от serial arduino
        # self.arduino = serial.Serial(self.com, self.name)

        # self.arduino.write(b'g')
        # time.sleep(0.1)
        # response = self.arduino.readline().decode().strip()
        # self.data.append(tuple(map(int, response.split(','))))

        # return self.data[-1]

        gyro_x = random.uniform(-1.3, -1.6)
        gyro_y = random.uniform(0.85, 0.95)
        gyro_z = random.uniform(0.25, 0.3)

        accel_x = random.uniform(0.2, 0.23)
        accel_y = random.uniform(-0.08, -0.13)
        accel_z = random.uniform(9.75, 9.85)

        # self.main_window.pritn_to_console(f'Data received: ({round(gyro_x, 3)}, {round(gyro_y, 3)}, {round(gyro_z, 3)}, {round(accel_x, 3)}, {round(accel_y, 3)}, {round(accel_z, 3)}) [OK]')

        return (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)

        
        

