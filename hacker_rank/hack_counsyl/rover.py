import bisect
import sys


STATE = "production"

"""
    Algorithm:-
    The algorithm is a basic dynamic programming implementation
    Basic Algorithm:-
    Assuming the blocks are sorted by start byte position.

    OPT(n, l) = minimum time required to download first n bytes
                considering 0:l blocks.
    Base Case -
    OPT(0, 0) = 0
    OPT(k, 0) = Infinity [For all k > 0]
    Recursive case -
    OPT(n, l) = min(OPT(n, l-1),
                    OPT(n - no_of_bytesin_l, l-1) + time_required_by_l.
    Solution :-
    OPT(Total_size, total_blocks)
    Runtime :-
    O(2^no_of_bits_to_write_total_size * no of blocks)

    We presented the above algorithm as it provides clarity in
    understanding the implemented algorithm.
    Implemented Algorithm:-
    Assuming the blocks are sorted by start byte position.
    Let l be block from bytes e - f
    OPT(l) = minimum time required to f bytes using 0 - l-1 blocks
             and always including the last block.
    OPT(0) = 0
    Solution-
    for all blocks B:
        if B end at total_bytes
            result = min(OPT(B), result)
    result is the answer
    Runtime -
    O(n^2)

    Design -
    ChunkTable -
    The class that represents the dynamic programming table
    Methods-
    get_time_downloading (no_of_bytes)
    min_time_downloading (no_of_bytes)
    add_downloading_time (start_position, end_position, time)
    Rover -
    get_meta_info()
    calculate_minimum_download_time()

    Possible Improvements:-
    a) We could implement the DP tablei(CHunkTable) as a tree which
    would make the algorithm take o(n*log(n)). Simplest method is
    to use Blist in blocks instead of list.
    b) As we can see from the profiling result provided below
       That if we create a tree structure which just returns the minimum
       time without iterating over a list we can use it improve the performance
       significantly.
    Profiling results to supporti claim (a) and (b):-
   Ordered by: standard name
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 bisect.py:1(<module>)
        1    0.000    0.000    0.444    0.444 rover.py:1(<module>)
     2000    0.002    0.000    0.004    0.000 rover.py:109(add_downloading_time)
        1    0.000    0.000    0.000    0.000 rover.py:125(Rover)
        1    0.000    0.000    0.008    0.008 rover.py:130(__init__)
        1    0.003    0.003    0.008    0.008 rover.py:134(get_meta_info)
     2000    0.000    0.000    0.000    0.000 rover.py:149(<lambda>)
        1    0.002    0.002    0.436    0.436 rover.py:151(calculate_minimum_download_time)
        1    0.000    0.000    0.000    0.000 rover.py:60(ChunkTable)
        1    0.000    0.000    0.000    0.000 rover.py:61(__init__)
     1999    0.001    0.000    0.002    0.000 rover.py:76(get_time_downloading)
  1018016    0.214    0.000    0.257    0.000 rover.py:90(block_generator)
     1999    0.171    0.000    0.430    0.000 rover.py:97(min_time_downloading)
     1999    0.001    0.000    0.001    0.000 {_bisect.bisect_left}
     2000    0.001    0.000    0.001    0.000 {_bisect.bisect_right}
  1018016    0.043    0.000    0.043    0.000 {len}
     2000    0.002    0.000    0.002    0.000 {map}
     2000    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
     4000    0.001    0.000    0.001    0.000 {method 'insert' of 'list' objects}
     2004    0.001    0.000    0.001    0.000 {method 'readline' of 'file' objects}
        1    0.001    0.001    0.001    0.001 {method 'sort' of 'list' objects}
     2000    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
"""


class ChunkTable:
    def __init__(self, total_byte_count):
        # Maintains the total byte_size so that min_total_time_downloading
        # can be pre cached
        self.total_byte_count = total_byte_count
        # Maintains the minimum total download time
        # Considering all blocks added till now
        self.min_total_download_time = float('inf')
        # This list maintains a just the end position
        # so that the blocks can searched till the point
        # using the C implemented bisect method
        self.block_end_positions = []
        # These are the entries corresponding to above values
        # The blocks are kept sorted by end position
        self.blocks = []

    def get_time_downloading(self, no_of_bytes):
        # NOTE:- Function is not multi threading safe
        # Last block has the maximum end time
        # This function returns a generator in the code
        last_block_end_position = self.block_end_positions[-1]
        if last_block_end_position < no_of_bytes:
            # Error no time for downloading till last block
            raise Exception("No Blocks found")
        # Get the start position for blocks which download
        # no_of_bytes
        start_position = bisect.bisect_left(self.block_end_positions,
                                            no_of_bytes)

        # Block generator
        def block_generator(start_position, blocks):
            while start_position < len(blocks):
                yield blocks[start_position]
                start_position += 1

        return block_generator(start_position, self.blocks)

    def min_time_downloading(self, no_of_bytes):
        # We get the minimum time among all the blocks which
        # end after the current byte
        min_time_required = float('inf')
        try:
            blocks = self.get_time_downloading(no_of_bytes)
        except Exception as e:
            return min_time_required
        # Select the block which takes minimum time
        for block in blocks:
            (b_start, b_end, time_required) = block
            if min_time_required > time_required:
                min_time_required = time_required
        return min_time_required

    def add_downloading_time(self, start, end, time_required):
        # saving for the total download time
        if end == self.total_byte_count and \
                time_required < self.min_total_download_time:
                    self.min_total_download_time = time_required

        # get the position to insert the block
        # as the blocks are kept sorted by end time
        selected_position = bisect.bisect_right(self.block_end_positions,
                                                end)
        self.block_end_positions.insert(selected_position,
                                        end)
        self.blocks.insert(selected_position,
                           (start, end, time_required))


class Rover:
    """
        Maintains the reading and processing of the file
        And runs the dynamic programming algorithm
    """
    def __init__(self, inp_stream):
        self.inp_stream = inp_stream
        self.get_meta_info()

    def get_meta_info(self):
        # Reading info from file
        self.total_bytes = int(self.inp_stream.readline())
        self.latency = int(self.inp_stream.readline())
        self.download_rate = int(self.inp_stream.readline())
        chunk_block_count = int(self.inp_stream.readline())
        self.blocks = []
        while chunk_block_count > 0:
            data = self.inp_stream.readline()
            (start, end) = map(int, data.split(','))
            time_required = float(end-start)/float(self.download_rate)
            time_required += 2*self.latency
            self.blocks.append((start, end, time_required))
            chunk_block_count -= 1
        # Sorting by start time
        self.blocks.sort(key=lambda x: x[0])

    def calculate_minimum_download_time(self):
        chunk_table = ChunkTable(self.total_bytes)
        for block in self.blocks:
            (start, end, time_required) = block
            # If start is the zero block no block is needed
            if start == 0:
                time_used_before = 0
            else:
                time_used_before = chunk_table.min_time_downloading(start)
            time_required += time_used_before
            chunk_table.add_downloading_time(start, end, time_required)
        total_downloadtime = chunk_table.min_total_download_time
        if total_downloadtime == float('inf'):
            raise Exception('No Complete Download possible')
        return total_downloadtime

if __name__ == "__main__":
    if STATE == "production":
        rover = Rover(sys.stdin)
        try:
            print "%0.3f" % (rover.calculate_minimum_download_time())
        except Exception as e:
            # As the problem statement says to print nothing
            pass
    if STATE == "unittest":
        # Chunk Table Testing
        TOTAL_BYTES = 1000
        chunk_table = ChunkTable(TOTAL_BYTES)
        # Test case 1
        chunk_table.add_downloading_time(0, 1000, 20)
        if chunk_table.min_time_downloading(100) == 20:
            print "Min Download time success"
        else:
            print "Min Download time failed"
        if chunk_table.min_time_downloading(2000) == float('inf'):
            print "Infinite download time success"
        else:
            print "Infinite download time failed"
        # Adding another block
        chunk_table.add_downloading_time(0, 1500, 10)
        if chunk_table.min_time_downloading(100) == 10:
            print "Extracting Min Download time success"
        else:
            print "Min Download time failed"
