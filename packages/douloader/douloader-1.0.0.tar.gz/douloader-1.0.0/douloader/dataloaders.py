import logging
import random
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue


def get_logger(name='douloader'):
    """
    douloader使用的打印日志插件
    :param name:
    :return:
    """

    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
    logger = logging.getLogger(name)
    return logger


class MultiDataLoaderBase(object):
    """
        此类是多进程读取数据的基类。
        现在的想法是后续针对不同数据、不同诉求的dataloader，只需要重写一些类就可以。
        """

    def __init__(self, config):
        self.run_type = ""
        self.multiple_ratio = 40
        self.sample_path_dict = dict()  # 用来存储所有的路径，包括Xma、Xgt等

        self.logger = get_logger("douloader")
        self.current_read_sample_index = 0
        self.current_true_sample_index = 0
        self.batch_size = config.batchSize
        self.add_threshold = self.batch_size * self.multiple_ratio  # 每次添加的数据的量
        self.max_threshold = self.batch_size * 80
        self.config = config

        # self.__shuffle__()

        # self.dataset_type = dataset_type
        # self.queue_max_size = 2  # The number of original data, not cropped data
        self.threading_pool_size = 3
        self.myThreadPool = ThreadPoolExecutor(max_workers=self.threading_pool_size)
        self.sample_index_mutex = threading.Lock()

        self.queue = Queue()

        self.adding_threading_number = 0  # 正在添加数据的线程数量，不控制的话会提交大量的提交数据任务
        self.adding_threading_number_mutex = threading.Lock()
        # self.add_data_to_queue()
        # if config.if_data_augmentation:
        #     self.preprocessModule = CustomPreprocessModule(configure.patch_size, configure.aug_probability)

        self.data_length = len(self.sample_path_dict[0])

    def __len__(self):
        length = int(self.data_length / self.batch_size)
        return length

    def __shuffle__(self):
        self.shuffled_index_list = [i for i in random.sample(range(0, self.data_length), self.data_length)]
        for path_list in self.sample_path_dict.values():
            path_list = [path_list[i] for i in self.shuffled_index_list]

    def prepare_sample_dict(self):
        """
        此方法用来构建存储data path的dict
        :return:
        """
        raise NotImplementedError

    def __iter__(self):
        self.current_read_sample_index = 0
        self.add_threshold = self.batch_size * self.multiple_ratio
        if self.run_type == "train":
            self.__shuffle__()
        return self

    def __next__(self):
        try:
            # one epoch finish
            if self.queue.qsize() < self.batch_size:
                if self.adding_threading_number == 0:  # 还没人在加  自己去读或者已经没有剩下的了
                    self.adding_threading_number_mutex.acquire()
                    self.adding_threading_number = self.adding_threading_number + 1
                    self.adding_threading_number_mutex.release()
                    read_index_list = self.__get_read_index__()
                    future = self.myThreadPool.submit(self.__add_data_to_queue__, read_index_list)
                    wait([future])  # 会阻塞  get_next_batch方法如果有剩余会继续添加，没有剩余会抛出异常

                    if future.result() is False:
                        del future
                        raise StopIteration
                next_batch = self.__get_next_batch__()
                return self.parse_obj_list(next_batch)
            # The rest is enough and supplement the queue if the rest if not enough after read a batch
            else:
                next_batch = self.__get_next_batch__()
                tmp_queue_size = self.queue.qsize()
                if tmp_queue_size < self.add_threshold and self.adding_threading_number < self.threading_pool_size:
                    self.logger.info(str(threading.current_thread()) + ": current queue size is " + str(
                        tmp_queue_size) + " need to add")
                    read_index_list = self.__get_read_index__()
                    self.adding_threading_number_mutex.acquire()
                    self.adding_threading_number = self.adding_threading_number + 1
                    self.adding_threading_number_mutex.release()
                    future = self.myThreadPool.submit(self.__add_data_to_queue__, read_index_list)
                return self.parse_obj_list(next_batch)
        except KeyboardInterrupt:
            print("catch the control c order!")
            self.myThreadPool.shutdown()

        # my_logger.info(str(len(tmp_data_list)) + " patches has been added to list")

    def __get_read_index__(self):

        self.sample_index_mutex.acquire()
        tmp_read_index_list = list()
        if (self.current_read_sample_index + self.add_threshold) > self.data_length:
            self.add_threshold = self.data_length - self.current_read_sample_index
        if self.add_threshold == 0:
            self.sample_index_mutex.release()
            return tmp_read_index_list
        for i in range(self.add_threshold):
            tmp_read_index_list.append(self.current_read_sample_index)
            self.current_read_sample_index = self.current_read_sample_index + 1
        self.sample_index_mutex.release()
        self.logger.info("Get reading index completely!")
        return tmp_read_index_list

    def __get_next_batch__(self):
        """
        此方法是私有方法，不允许被重写
        :return: 返回一个batch大小的list，其中包含的是原始的填入到queue中的对象
        """
        obj_list = list()

        for i in range(self.batch_size):
            data = self.queue.get()
            self.queue.task_done()
            obj_list.append(data)
        return obj_list

    def __add_data_to_queue__(self, add_index_list):
        """
        不允许被重写
        此方法用来使用子类实现的方法来获得添加到queue中的一个object，
        List，Tuple，Dict，或者自己编写的类都可以。
        :param add_index_list: 需要往queue中添加的数据的index。
        :return:
        """
        if len(add_index_list) == 0:
            self.adding_threading_number_mutex.acquire()
            self.adding_threading_number = self.adding_threading_number - 1
            self.adding_threading_number_mutex.release()
            return False
        self.logger.info("start to add " + str(len(add_index_list)) + " samples to queue!")

        for ii in add_index_list:
            data_obj = self.read_one_data(ii)
            self.queue.put(data_obj)

        self.adding_threading_number_mutex.acquire()
        self.adding_threading_number = self.adding_threading_number - 1
        self.adding_threading_number_mutex.release()
        # self.queue_operator_mutex.release()

        self.logger.info("After adding, current size of queue is " + str(int(self.queue.qsize())))
        self.logger.info(
            "The current sample index is " + str(self.current_read_sample_index) + "/" + str(self.data_length))
        return True

    def read_one_data(self, add_index):
        """

        :param add_index:
        :return:
        """
        raise NotImplementedError

    def parse_obj_list(self, return_obj_list):
        """
        此方法可以被重写，来定制化一些自己想要的操作
        :param return_obj_list:
        :return:
        """
        return return_obj_list
