from multiprocessing import Process
import bot
import monitoring

if __name__ == '__main__':
    p1 = Process(target=bot.run_bot)
    p2 = Process(target=monitoring.start_monitoring)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
