import re

HAPROXY_HTTPLOG_CLF = r'^(\d+.\d+.\d+.\d+) - - \[(.*)\] \"(.*[01])\" (\d{3}) (\d+) \"\" \"\" (\d+) (\d{3}) \"([0-9a-zA-Z_\-]+)(~?)\" \"([0-9a-zA-Z_\-]+)\" \"([0-9a-zA-Z_\-><]+)\" (-?\d+) (-?\d+) (-?\d+) (-?\d+) (\d+) ([a-zA-Z\-]{4}) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) \"(.*?)\" \"(.*?)\" (.*)'
HAPROXY_HC_RE = re.compile(HAPROXY_HTTPLOG_CLF)

class Haproxy_Log:
    def __init__(self, extracted_log_obj):
        extracted_log = extracted_log_obj.groups()
        self.source_ip = extracted_log[0]
        self.req_time = extracted_log[1]
        self.req = extracted_log[2]
        self.status_code = extracted_log[3]
        # sent from server -> client
        self.bytes_sent = extracted_log[4]
        self.client_port = extracted_log[5]
        self.request_micros = extracted_log[6]
        self.frontend_name = extracted_log[7]
        self.ssl = extracted_log[8]
        self.backend_name = extracted_log[9]
        self.server_name = extracted_log[10]
        #time waiting in various states
        self.time_full_request = extracted_log[11]
        self.time_queue_wait = extracted_log[12]
        self.time_server_conn = extracted_log[13]
        self.time_resp_headers = extracted_log[14]
        self.time_total = extracted_log[15]
        self.termination_state = extracted_log[16]
        # number of concurrent conn to the process at log time
        self.actconn = extracted_log[17]
        self.frontend_conns = extracted_log[18]
        self.backend_conns = extracted_log[19]
        self.server_conns = extracted_log[20]
        self.retries = extracted_log[21]
        self.server_queue = extracted_log[22]
        self.backend_queue = extracted_log[23]
        self.cap_req_cookie = extracted_log[24]
        self.cap_resp_cookie = extracted_log[25]
        #could include captured response headers
        self.cap_req_headers = extracted_log[26]

def parse_haproxy_clf_line(line):
    extraction = HAPROXY_HC_RE.search(line)
    if extraction:
        ext = Haproxy_Log(extraction)
#        print "FOUND: {}".format(Haproxy_Log(extraction).__dict__)
        return True
    else:
        print line
        return False
#        print "NOT FOUND!"

def tail(f, lines):
    '''
    Seek to beginning of line that is $lines from EOF
    '''
    lines_wanted = lines
    f.seek(0, 2) 
    last_pos = f.tell()

def main():
    fin = open('haproxy.log', 'r')
    line_count = 0
    failed_lines = 0
    for line in fin:
        suc = parse_haproxy_clf_line(line)
        if not suc:
            failed_lines += 1
        line_count += 1
#    for x in range(0,10):
#        parse_haproxy_clf_line(fin.readline())
    print "DONE"
    print "Lines processed: {}".format(line_count)
    print "Lines failes: {}".format(failed_lines)
    fin.close()

if __name__ == '__main__':
    main()
