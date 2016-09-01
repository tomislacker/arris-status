from lxml import html


class Parser(object):
    @classmethod
    def parse(cls, contents):
        raise NotImplementedError

    @classmethod
    def sanitize_name(cls, name):
        return name


class Status(Parser):
    uri = '/cgi-bin/status_cgi'

    @classmethod
    def parse(cls, contents):
        tree = html.fromstring(contents)
        data = {}

        # Downstream channels
        dchans = []
        dchan_rows = tree.xpath('/html/body/div[1]/div[3]/table[2]//tr')
        headers = [cls.sanitize_name(td.text) for td in dchan_rows[0].xpath('td')[1:]]

        for row in dchan_rows[1:]:
            dchan = {}
            for col_idx, td in enumerate(row.xpath('td')[1:]):
                dchan.update({
                    headers[col_idx]: td.text,
                })
            dchans.append(dchan)
        data.update({'downstream': dchans})

        # Upstream channels
        uchans = []
        uchan_rows = tree.xpath('/html/body/div[1]/div[3]/table[4]//tr')
        headers = [cls.sanitize_name(td.text) for td in uchan_rows[0].xpath('td')[1:]]

        for row in uchan_rows[1:]:
            uchan = {}
            for col_idx, td in enumerate(row.xpath('td')[1:]):
                uchan.update({
                    headers[col_idx]: td.text,
                })
            uchans.append(uchan)
        data.update({'upstream': uchans})

        # System status
        sys_stat = {}
        for row in tree.xpath('/html/body/div[1]/div[3]/table[6]//tr'):
            cols = row.xpath('td')
            sys_stat.update({
                cls.sanitize_name(cols[0].text): cols[1].text.strip(),
            })
        data.update({'system': sys_stat})

        # Interface parameters
        ifaces = []
        ifaces_rows = tree.xpath('/html/body/div[1]/div[3]/table[8]//tr')
        headers = [cls.sanitize_name(td.text) for td in ifaces_rows[0].xpath('td')]

        for row in ifaces_rows[1:]:
            iface = {}
            for col_idx, td in enumerate(row.xpath('td')):
                iface.update({
                    headers[col_idx]: td.text,
                })
            ifaces.append(iface)
        data.update({'ifaces': ifaces})

        return data


class Hardware(Parser):
    uri = '/cgi-bin/vers_cgi'


class Events(Parser):
    uri = '/cgi-bin/event_cgi'

class State(Parser):
    uri = '/cgi-bin/cm_state_cgi'

    @classmethod
    def parse(cls, contents):
        tree = html.fromstring(contents)
        data = {}


        # CM State
        data.update({
            'cm_state': ''.join(tree.xpath('/html/body/div[1]/div[3]/p[1]/text()')).strip(),
        })

        # Telephony data
        telephony_data = {}
        for row in tree.xpath('/html/body/div[1]/div[3]/table[1]/tbody/tr'):
            cols = row.xpath('td')
            telephony_data.update({
                cls.sanitize_name(cols[0].text): cols[1].text.strip(),
            })
        data.update({'telephony': telephony_data})

        # TOD state
        tod_data = {}
        for row in tree.xpath('/html/body/div[1]/div[3]/table[2]/tbody/tr'):
            cols = row.xpath('td')
            tod_data.update({
                cls.sanitize_name(cols[0].text): cols[1].text.strip(),
            })
        data.update({'tod': tod_data})

        # BPI State
        bpi_data = {}
        for row in tree.xpath('/html/body/div[1]/div[3]/table[3]/tbody/tr'):
            cols = row.xpath('td')
            bpi_data.update({
                cls.sanitize_name(cols[0].text): cols[1].text.strip(),
            })
        data.update({'bpi': bpi_data})

        # DHCP attempts
        dhcp_data = {}
        for row in tree.xpath('/html/body/div[1]/div[3]/table[4]/tbody/tr'):
            cols = row.xpath('td')
            dhcp_data.update({
                cls.sanitize_name(cols[0].text): cols[1].text.strip(),
            })
        data.update({'dhcp': dhcp_data})

        # Power supply telemetry
        ps_data = {}
        ps_rows = tree.xpath('/html/body/div[1]/div[3]/table[5]//tr')
        ps_cols = ps_rows[1].xpath('td')
        for idx, header_col in enumerate(ps_rows[0].xpath('td/b')):
            ps_data.update({
                cls.sanitize_name(header_col.text): ps_cols[idx].text,
            })
        data.update({'power': ps_data})

        return data
