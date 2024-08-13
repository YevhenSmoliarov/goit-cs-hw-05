import requests
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import re
import multiprocessing as mp
from functools import reduce


def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні тексту: {e}")
        return None


def map_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def reduce_counts(counters):
    return reduce(lambda c1, c2: c1 + c2, counters)

def mapreduce(text, num_threads):
    chunks = [text[i::num_threads] for i in range(num_threads)]
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        counters = list(executor.map(map_words, chunks))
    return reduce_counts(counters)


def visualize_top_words(word_counts, top_n=10):
    common_words = word_counts.most_common(top_n)
    words, counts = zip(*common_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(f"Топ {top_n} слів за частотою використання")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.show()



if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Замість цього введіть свою URL-адресу
    num_threads = mp.cpu_count()  # Кількість потоків дорівнює кількості ядер процесора
    
    text = fetch_text_from_url(url)
    
    if text:
        word_counts = mapreduce(text, num_threads)
        visualize_top_words(word_counts, top_n=10)



pip install requests matplotlib


