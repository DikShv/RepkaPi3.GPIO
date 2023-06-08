import RepkaPi.GPIO as GPIO

if __name__ == "__main__":

    PWM_chip = 0
    PWM_pin = 0
    frequency_Hz = 3800
    Duty_Cycle_Percent = 100

    p = GPIO.PWM(PWM_chip, PWM_pin, frequency_Hz, Duty_Cycle_Percent)    # new PWM on channel=LED_gpio frequency=38KHz

    print("Нажмите любую кнопку для запуска PWM0/ШИМ0")
    input()
    p.start_pwm()

    print("заполнить на 50 PWM/ШИМ, нажав кнопку")
    input()
    p.duty_cycle(50)

    print("изменить частоту PWM/ШИМ, нажав кнопку")
    input()
    p.change_frequency(500)

    print("остановить PWM/ШИМ, уменьшив до 0, нажав кнопку")
    input()
    p.stop_pwm()

    print("изменить полярность нажатием кнопки")
    input()
    p.pwm_polarity()

    print("увеличьте до 75, но чтобы свет был тусклым. нажмите кнопку, чтобы продолжить")
    input()
    p.duty_cycle(75)

    print("уменьшить до 25, нажмите кнопку, чтобы продолжить")
    input()
    p.duty_cycle(25)

    print("остановите PWM/ШИМ (он был инвертирован, поэтому он должен быть на полную яркость), нажмите кнопку, чтобы продолжить")
    input()
    p.stop_pwm()

    print("удалить объект и деактивировать вывод PWM/ШИМ, нажмите кнопку, чтобы продолжить")
    input()
    p.pwm_close()
    del p  # delete the class
