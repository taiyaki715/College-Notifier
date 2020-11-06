from notifier import Scraper, Notifier


class Main:
    def __init__(self):
        self.scraper = Scraper('c0b2001256@edu.teu.ac.jp', 'ix%j86qsC')
        self.notifier = Notifier('ow1snOdCNyTHIUsfOLxwp3w9anjqEkm2UJJLjEm3rO0')

    def run(self):
        news_list = self.scraper.get_news()

        message = '■' + '\n■'.join(news_list)
        self.notifier.send(message)


if __name__ == '__main__':
    main = Main()
    main.run()
