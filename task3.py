from threading import Thread
from threading import BoundedSemaphore
from time import sleep, time
from random import randint
a = time()
get_data_sem = BoundedSemaphore(10)
write_to_file_sem = BoundedSemaphore(5)
write_to_console_sem = BoundedSemaphore(1)
def sem_wrapper_maker(sem):
    def sem_wrapper(f):
        def wrapper(task_id):
            sem.acquire()
            f(task_id)
            sem.release()
        return wrapper
    return sem_wrapper
@sem_wrapper_maker(get_data_sem)
def get_data(task_id):
    print(f"processing get_data({task_id})")
    sleep(randint(1, 3))
    print(f"completed get_data({task_id})")
@sem_wrapper_maker(write_to_file_sem)
def write_to_file(task_id):
    print(f"processing write_to_file({task_id})")
    sleep(randint(1, 5))
    print(f"completed write_to_file({task_id})")
@sem_wrapper_maker(write_to_console_sem)
def write_to_console(task_id):
    print(f"processing write_to_console({task_id})")
    sleep(randint(1, 5))
    print(f"completed write_to_console({task_id})")
def handle_task(task_id):
    get_data(task_id)
    to_file = Thread(target=write_to_file, args=(task_id,))
    to_console = Thread(target=write_to_console, args=(task_id,))
    to_file.start()
    to_console.start()
    to_file.join()
    to_console.join()
if __name__ == '__main__':
    threads = [Thread(target=handle_task, args=(task_id,)) for task_id in range(1, 21)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
print(time() - a)