import re


class Episode:
    def __init__(self, episode_id, title, url_thumbnail, rating, created_date):
        self.episode_id = episode_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self.rating = rating
        self.created_date = created_date

    def __repr__(self):
        return self.title

    @classmethod
    def create_from_soup(cls, soup):
        """
        받는 soup의 Selector: 'table.viewList tr'
        :param soup: BeautifulSoup객체 또는
                     BeautifulSoup객체에서 'select', 'find'등의 메서드를 사용해 리턴된 Tag객체
        :return: Episode 인스턴스
        """
        try:
            td_list = soup.select('td')
            href = td_list[0].select_one('a')['href']

            no = re.search(r'no=(\d+)', href).group(1)
            url_thumbnail = td_list[0].select_one('img')['src']
            title = td_list[1].select_one('a').get_text(strip=True)
            rating = td_list[2].select_one('strong').get_text()
            created_date = td_list[3].get_text(strip=True)

            return cls(
                episode_id=no,
                title=title,
                url_thumbnail=url_thumbnail,
                rating=rating,
                created_date=created_date,
            )
        except:
            # 로그를 쌓으면 좋음
            raise EpisodeCreateFromSoupError(soup)


class EpisodeCreateFromSoupError(Exception):
    def __init__(self, soup):
        self.soup = soup

    def __str__(self):
        return f'HTML로부터 Episode를 생성하는데 실패했습니다.'
