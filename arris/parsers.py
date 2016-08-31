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
    fields = {
        'uptime': '/html/body/div[1]/div[3]/table[6]/tbody/tr[1]/td[2]',
    }


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
