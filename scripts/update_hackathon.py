import os
import re
from datetime import datetime, timezone, timedelta

# 全局配置
# 结束时间配置 (UTC+8 时区)
END_TIME_UTC8 = "2025-07-20 18:00:00"  # 格式: YYYY-MM-DD HH:MM:SS

def extract_field(content, field_name):
    """Extract a field value from the content using regex."""
    pattern = rf'{field_name}:\s*[\'"]([^\'"]*)[\'"]'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return ""

def check_project_submitted(participant_dir):
    """Check if participant has submitted project by looking for files in project folder."""
    project_dir = os.path.join(participant_dir, 'project')
    if os.path.exists(project_dir):
        # Check if there are any files in the project directory
        files = [f for f in os.listdir(project_dir) if os.path.isfile(os.path.join(project_dir, f))]
        return len(files) > 0
    return False

def check_nft_image_exists(name):
    """Check if NFT image exists for the participant."""
    nft_path = os.path.join(os.getcwd(), 'materials', 'NFT', f'{name}.png')
    return os.path.exists(nft_path)

def parse_participant_file(file_path):
    """Parse a participant README.md file and extract relevant fields."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            if "name:" in content:
                participant_dir = os.path.dirname(file_path)
                participant_name = os.path.basename(participant_dir)
                
                return {
                    'type': 'registration',
                    'name': extract_field(content, 'name'),
                    'description': extract_field(content, 'description'),
                    'contact_method': extract_field(content, 'contact_method'),
                    'contact': extract_field(content, 'contact'),
                    'wallet_address': extract_field(content, 'wallet_address'),
                    'role': extract_field(content, 'role'),
                    'timezone': extract_field(content, 'timezone'),
                    'team_name': extract_field(content, 'team_name'),
                    'team_status': extract_field(content, 'team_status'),
                    'team_members': extract_field(content, 'team_members'),
                    'project_name': extract_field(content, 'project_name'),
                    'project_description': extract_field(content, 'project_description'),
                    'project_progress': extract_field(content, 'project_progress'),
                    'tech_stack': extract_field(content, 'tech_stack'),
                    'support_needed': extract_field(content, 'support_needed'),
                    'goals': extract_field(content, 'goals'),
                    'notes': extract_field(content, 'notes'),
                    'file_path': file_path,
                    'participant_dir': participant_dir,
                    'project_submitted': check_project_submitted(participant_dir)
                }
            else:
                print(f"Unknown file type: {file_path}")
                return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def scan_participants_directory():
    """Scan the participants directory for participant folders."""
    participants_dir = os.path.join(os.getcwd(), 'participants')
    if not os.path.exists(participants_dir):
        print(f"Participants directory not found: {participants_dir}")
        return []
    
    participants = []
    participant_folders = []
    
    # Get all subdirectories in participants folder with creation time
    for item in os.listdir(participants_dir):
        item_path = os.path.join(participants_dir, item)
        if os.path.isdir(item_path) and item != 'template':
            readme_path = os.path.join(item_path, 'README.md')
            if os.path.exists(readme_path):
                # Get folder creation time (ctime)
                creation_time = os.path.getctime(item_path)
                participant_folders.append((item_path, creation_time))
    
    # Sort by creation time (oldest first - ascending order)
    participant_folders.sort(key=lambda x: x[1])
    
    print(f"Participants sorted by creation time:")
    for item_path, creation_time in participant_folders:
        folder_name = os.path.basename(item_path)
        creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {folder_name}: {creation_date}")
    
    # Parse participant files in sorted order
    for item_path, _ in participant_folders:
        readme_path = os.path.join(item_path, 'README.md')
        data = parse_participant_file(readme_path)
        if data and data['type'] == 'registration':
            participants.append(data)
    
    return participants

def generate_participants_content(participants):
    """Generate participants content in the new format."""
    if not participants:
        return "<!-- No participants registered yet -->"
    
    # 解析结束时间配置
    end_time_utc8 = datetime.strptime(END_TIME_UTC8, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(timedelta(hours=8)))
    current_time_utc8 = datetime.now(timezone(timedelta(hours=8)))
    
    content = ""
    
    for i, participant in enumerate(participants):
        name = participant.get('name', '')
        contact = participant.get('contact', '')
        contact_method = participant.get('contact_method', '')
        role = participant.get('role', '')
        timezone_info = participant.get('timezone', '')
        description = participant.get('description', '')
        project_name = participant.get('project_name', '')
        project_description = participant.get('project_description', '')
        project_progress = participant.get('project_progress', '')
        team_members = participant.get('team_members', '')
        project_submitted = participant.get('project_submitted', False)
        
        # Determine participation type
        if team_members and ',' in team_members:
            participation_type = "Team"
            members_display = team_members
        else:
            participation_type = "Solo"
            members_display = name if name else "~"
        
        # Progress 只显示 project_progress 字段，不关联是否已提交
        if project_progress:
            progress = project_progress
        else:
            progress = "~"
        
        # 判断状态：如果超过结束时间且未提交，则显示未提交
        if current_time_utc8 > end_time_utc8:
            if project_submitted:
                status = "✅ Submitted"
            else:
                status = "❌ Unsubmitted"
        else:
            if project_submitted:
                status = "✅ Submitted"
            else:
                status = "⏳ Active"
        
        # Check if NFT image exists
        nft_exists = check_nft_image_exists(name)
        
        # Generate contact display
        contact_display = contact
        if contact and contact_method:
            contact_display = f'`💬 {contact_method}: {contact}`'
        elif not contact or not contact_method:
            contact_display = "~"
        
        # Generate role display
        role_display = f'`🔧 {role}`' if role else '~'
        
        # Generate timezone display
        timezone_display = f'`🕐 {timezone_info}`' if timezone_info else '~'
        
        # Generate project section
        project_section = ""
        if project_name:
            project_section = f"\n##### Project: {project_name}"
            if project_description:
                project_section += f"\n- *{project_description}* [📁](./participants/{name}/project/)"
        
        # Generate table with conditional NFT column
        if nft_exists:
            table = f"""
<table>
<tr>
    <th align="center">🧩 Participation</th>
    <th align="center">💪 Members</th>
    <th align="center">🏁 Progress</th>
    <th align="center">🌱 Status </th>
    <th align="center">🏅 NFT Badge </th>
</tr>
<tr>
    <td align="center">{participation_type}</td>
    <td align="center">{members_display}</td>
    <td align="center">{progress}</td>
    <td align="center">{status}</td>
    <td align="center"><img src="./materials/NFT/{name}.png" alt="{name}" width="200" /></td>
</tr>
</table>"""
        else:
            table = f"""
<table>
<tr>
    <th align="center">🧩 Participation</th>
    <th align="center">💪 Members</th>
    <th align="center">🏁 Progress</th>
    <th align="center">🌱 Status </th>
</tr>
<tr>
    <td align="center">{participation_type}</td>
    <td align="center">{members_display}</td>
    <td align="center">{progress}</td>
    <td align="center">{status}</td>
</tr>
</table>"""
        
        # Combine all parts with separator only at the bottom
        # Check if this is the last participant
        is_last = (i == len(participants) - 1)
        
        if is_last:
            # Last participant - no separator
            participant_content = f"""#### 👤 {name}

{contact_display}  {role_display}  {timezone_display}  
- *{description}* [🔗](./participants/{name}/README.md) {project_section}  {table}

"""
        else:
            # Not the last participant - add separator
            participant_content = f"""#### 👤 {name}

{contact_display}  {role_display}  {timezone_display}  
- *{description}* [🔗](./participants/{name}/README.md) {project_section}  {table}

---

"""
        
        content += participant_content
    
    return content

def update_participants_section(participants, readme_path):
    """Update the participants section in the README file."""
    
    participants_content = generate_participants_content(participants)
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for the participants section and everything until the next section
        pattern = r'(## 📝 Participants)\s*([\s\S]*?)(?=\n## |\Z)'
        
        match = re.search(pattern, content)

        if match:
            # Replace existing participants section completely
            updated_content = re.sub(
                pattern,
                r'\1' + f"\n\n{participants_content}",
                content
            )
        else:
            # Add participants section before the co-organizers section
            insertion_pattern = r'(## 🤝 Co-organizers)'
            
            if re.search(insertion_pattern, content):
                updated_content = re.sub(
                    insertion_pattern,
                    f"## 📝 Participants\n\n{participants_content}\n\n" + r'\1',
                    content
                )
            else:
                # If no insertion point found, append at the end
                updated_content = content + f"\n\n## 📝 Participants\n\n{participants_content}\n"

        # Update timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_content = re.sub(
            r'_Last updated: .*_',
            f"_Last updated: {timestamp}_",
            updated_content
        )

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"Updated participants section in {os.path.basename(readme_path)}")
        return True
    except Exception as e:
        print(f"Error updating {readme_path}: {e}")
        return False

def update_hackathon():
    """Update the hackathon README file with participant information."""
    participants = scan_participants_directory()
    
    print(f"Found {len(participants)} participants")

    # Update main README
    readme_path = os.path.join(os.getcwd(), 'README.md')
    if os.path.exists(readme_path):
        update_participants_section(participants, readme_path)
    else:
        print(f"README not found: {readme_path}")

    print(f"Updated README file with {len(participants)} participants.")
    return True

if __name__ == '__main__':
    import sys
    
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Usage:")
            print("  python update_hackathon.py                  # 更新参与者信息")
            print("  python update_hackathon.py --help           # 显示帮助信息")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # 执行更新操作
        update_hackathon()