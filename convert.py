import os
import json
import yaml

def main():
    if not os.path.exists('custom.yaml'):
        print("未找到 custom.yaml 文件")
        return

    with open('custom.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    payload = data.get('payload', [])
    sb_rules = {
        "domain": [],
        "domain_suffix": [],
        "domain_keyword": [],
        "ip_cidr": []
    }

    for item in payload:
        parts = item.split(',')
        if len(parts) < 2:
            continue
        rule_type = parts[0].strip().upper()
        rule_value = parts[1].strip()

        if rule_type == 'DOMAIN':
            sb_rules["domain"].append(rule_value)
        elif rule_type == 'DOMAIN-SUFFIX':
            sb_rules["domain_suffix"].append(rule_value)
        elif rule_type == 'DOMAIN-KEYWORD':
            sb_rules["domain_keyword"].append(rule_value)
        elif rule_type in ['IP-CIDR', 'IP-CIDR6']:
            sb_rules["ip_cidr"].append(rule_value)

    # 过滤掉空的规则分类
    cleaned_rules = {k: v for k, v in sb_rules.items() if v}

    output_json = {
        "version": 1,
        "rules": [cleaned_rules]
    }

    with open('custom.json', 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)
    print("已成功转换为 custom.json")

if __name__ == '__main__':
    main()
