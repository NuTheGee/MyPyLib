import re

def Parse(form, data):
    if "trunc" in form.keys():
        match = re.findall(form["trunc"], data, re.DOTALL)
        if len(match) > 0:
            data = match[0]
    if "split" in form.keys():
        match = re.findall(form["split"], data, re.DOTALL)
        if len(match) > 0:
            data = match
    else:
        data = [data]
    result = list()
    for row in data:
        temp = dict()
        for item in form["items"]:
            match = re.findall(item[1], row)
            if len(match) == 1:
                match = match[0]
                for sub in form["sub"]:
                    match = re.sub(sub[0], sub[1], match)
                temp[item[0]] = match
            else:
                temp[item[0]] = ""
        result.append(temp)
    return result


def HTMLTable(form, data):
    # 중첩된 테이블이 아닌 경우
    # 1. 특정 테이블 잘라내기
    match = re.findall("(<table.+?</table>)", data, re.DOTALL)
    print("{} tables".format(len(match)))
    assert "index" in form.keys() and form["index"] in range(0, len(match))
    table = match[form["index"]]
    # 1.1 테이블 본문 잘라내기
    if "tbody" in form.keys() and form["tbody"]:
        match = re.findall("(<tbody.+?</tbody>)", table, re.DOTALL)
        assert len(match) == 1
        table = match[0]
    # 2. 행으로 나누기
    rows = re.findall("<tr.*?>\s*(.*?)\s*</tr>", table, re.DOTALL)
    print("{} rows".format(len(rows)))
    # 2.1 no result
    if "none" in form.keys() and form["none"](rows): return list()
    # 3. 각 행을 셀로 나누기
    result = list()
    for row in rows:
        items = re.findall("<td.*?>\s*(.*?)\s*</td>", row, re.DOTALL)
        result.append(items)
    # 3.1 사전형으로 변환
    if "dict" in form.keys():
        result_dict = list()
        for row in result:
            temp = dict()
            for item in form["dict"]:
                assert len(item) in [2, 3]
                if len(item) == 2:
                    temp[item[0]] = row[item[1]].strip()
                else:
                    temp[item[0]] = item[2](row[item[1]].strip())
            result_dict.append(temp)
        return result_dict
    else:
        return result

def RowFormat(form, row):
    # Dict -> Dict: 두 단계로 나누어 진행
    assert len(form) == 2
    result = dict()
    # 첫번째 단계: 기본 변환
    first = form[0]
    for item in first:
        assert len(item) in [2, 3]
        if len(item) == 3:
            result[item[0]] = item[2](row[item[1]])
        else:
            result[item[0]] = row[item[1]]
    # 두번째 단계: 확장 변환
    second = form[1]
    for item in second:
        result[item[0]] = item[1](result)
    return result