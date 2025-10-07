#!/usr/bin/env node

/**
 * 更新README中的链接
 * Update links in README.md
 */

const fs = require('fs');
const path = require('path');
const { FIELD_NAMES, GITHUB_CONFIG, REQUIRED_FIELDS } = require('./config/constants');

// 获取命令行参数
const args = process.argv.slice(2);
const repoUrl = args[0] || GITHUB_CONFIG.REPO_URL;

console.log('🔗 正在更新README中的链接...');
console.log(`📦 仓库URL: ${repoUrl}`);

// 生成链接的函数
function generateIssueUrl(title, body) {
    const encodedTitle = encodeURIComponent(title);
    const encodedBody = encodeURIComponent(body);
    return `${repoUrl}/issues/new?title=${encodedTitle}&body=${encodedBody}`;
}

const NOTE = `> 📝 **Please fill in the content after ">"**`;

// 生成带必填标识的字段
function generateFieldWithRequired(fieldName, description, fieldType) {
    const requiredFields = REQUIRED_FIELDS[fieldType];
    const isRequired = requiredFields.includes(fieldName);
    const requiredMark = isRequired ? ' | Required' : '';
    return `**${fieldName}** (${description}${requiredMark})`;
}

// 生成注册链接
const registrationLink = generateIssueUrl(`${GITHUB_CONFIG.ISSUE_TITLE_PREFIXES.REGISTRATION} - New`, `## Registration Form

${NOTE}

${generateFieldWithRequired(FIELD_NAMES.REGISTRATION.NAME, 'Please enter your full name', 'REGISTRATION')}
>

${generateFieldWithRequired(FIELD_NAMES.REGISTRATION.DESCRIPTION, 'Brief personal introduction including skills and experience', 'REGISTRATION')}
>

${generateFieldWithRequired(FIELD_NAMES.REGISTRATION.CONTACT, 'Format: Contact Method: Contact Account, e.g., Telegram: @username, WeChat: username, Email: email@example.com', 'REGISTRATION')}
>

${generateFieldWithRequired(FIELD_NAMES.REGISTRATION.WALLET_ADDRESS, 'Your wallet address or ENS domain on Ethereum mainnet', 'REGISTRATION')}
>

${generateFieldWithRequired(FIELD_NAMES.REGISTRATION.TEAM_WILLINGNESS, 'Choose one: Yes | No | Maybe', 'REGISTRATION')}
>`);

// 生成提交链接
const submissionLink = generateIssueUrl(`${GITHUB_CONFIG.ISSUE_TITLE_PREFIXES.SUBMISSION} - New`, `## Project Submission Form

${NOTE}

${generateFieldWithRequired(FIELD_NAMES.SUBMISSION.PROJECT_NAME, 'Enter your project name', 'SUBMISSION')}
>

${generateFieldWithRequired(FIELD_NAMES.SUBMISSION.PROJECT_DESCRIPTION, 'Brief description about your project in one sentence', 'SUBMISSION')}
>

${generateFieldWithRequired(FIELD_NAMES.SUBMISSION.PROJECT_LEADER, 'Project leader name', 'SUBMISSION')}
>

${generateFieldWithRequired(FIELD_NAMES.SUBMISSION.PROJECT_MEMBERS, 'List all team members, comma-separated', 'SUBMISSION')}
>

${generateFieldWithRequired(FIELD_NAMES.SUBMISSION.REPOSITORY_URL, 'Open source repository URL - project must be open source', 'SUBMISSION')}
>`);

console.log('\n📝 生成的链接:');
console.log('注册链接:', registrationLink);
console.log('提交链接:', submissionLink);

// 读取README文件
const readmePath = path.join(__dirname, '../../README.md');
let readmeContent = fs.readFileSync(readmePath, 'utf8');

// 更新注册链接（替换注释标记之间的所有内容）
const registrationPattern = /(<!-- Registration link start -->)[\s\S]*?(<!-- Registration link end -->)/;
const newRegistrationContent = `$1\n[Register ➡️](${registrationLink})\n$2`;
readmeContent = readmeContent.replace(registrationPattern, newRegistrationContent);

// 更新提交链接（替换注释标记之间的所有内容）
const submissionPattern = /(<!-- Submission link start -->)[\s\S]*?(<!-- Submission link end -->)/;
const newSubmissionContent = `$1\n\n[Submit ➡️](${submissionLink})\n\n$2`;
readmeContent = readmeContent.replace(submissionPattern, newSubmissionContent);

// 写回文件
fs.writeFileSync(readmePath, readmeContent, 'utf8');

console.log('\n✅ README链接更新完成！');
console.log('📄 文件路径:', readmePath);