import java.time.LocalDate;

public class Sorts {
    public static void main(String[] args) {
        for (int i = 0; i < 100; i++) {
            int acc = 0;
            for (int j = 0; j < 100; j++) {
                acc += test_xor_swap_time(i*1000);
            }
        }
        System.out.println(acc/100);
    }

    public void test_xor_swap_time(int num) {
        int[] nums = [0, num]
        LocalDate start = LocalDate.now()
        for (int i = 0; i < 10000; i++) {
            xor_swap(nums, 0, 1);
        }
        return LocalDate.now() - start
    }


    public void xor_swap(int[] my_list, int a, int b) {
        my_list[a] ^= my_list[b];
        my_list[b] ^= my_list[a];
        my_list[a] ^= my_list[b];
    }
}