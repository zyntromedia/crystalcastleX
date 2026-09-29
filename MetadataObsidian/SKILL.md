
การดึงรายการไฟล์ทั้งหมดที่มีแท็กหรือ Metadata เฉพาะใน Obsidian Vault.md
การดึงรายการไฟล์ทั้งหมดที่มีแท็กหรือ Metadata เฉพาะใน Obsidian Vault

---
title: การดึงรายการไฟล์ทั้งหมดที่มีแท็กหรือ Metadata เฉพาะใน Obsidian Vault
aliases:
  - Obsidian Search Files by Tag
  - Obsidian Search Files by Metadata
  - Obsidian Vault Metadata Query
  - Obsidian MetadataCache Search
  - Obsidian Find Notes by Tag
  - Query Obsidian Vault TypeScript
  - ค้นหาโน้ตตามแท็ก Obsidian
  - ค้นหาไฟล์ตาม Metadata Obsidian
tags:
  - obsidian
  - obsidian/api
  - obsidian/metadata
  - obsidian/tags
  - obsidian/plugins
  - typescript
  - vault
  - search
  - automation
  - ai-agents
status: active
note_type: code-guide
topic: Querying Obsidian vault files by tag and metadata
language: th
created: 2026-09-29
updated: 2026-09-29
reviewed: false
security_level: internal
audience:
  - plugin-developer
  - typescript-developer
  - agent-developer
  - obsidian-user
api_surface:
  - Vault
  - MetadataCache
  - CachedMetadata
operations:
  - getMarkdownFiles
  - getFileCache
  - filter-by-tag
  - filter-by-frontmatter
  - filter-by-alias
  - filter-by-path
contains_secrets: false
contains_credentials: false
related:
  - "[[การดึง Metadata และ Frontmatter ผ่าน Obsidian MetadataCache API]]"
  - "[[Obsidian AGENTS API Knowledge Documents]]"
  - "[[ตัวอย่างโค้ด TypeScript สำหรับเชื่อมต่อ AI Agent กับ Obsidian Plugin API]]"
  - "[[Obsidian Database Migration]]"
  - "[[Obsidian Graph View]]"
daily_note: "[[2026-09-29]]"
created_daily_note: "[[2026-09-29]]"
updated_daily_note: "[[2026-09-29]]"
cssclasses:
  - technical-note
  - code-note
---

# การดึงรายการไฟล์ทั้งหมดที่มีแท็กหรือ Metadata เฉพาะใน Obsidian Vault

> [!abstract]
> ใช้ `app.vault.getMarkdownFiles()` เพื่อดึง Markdown files ทั้งหมดใน Obsidian Vault แล้วใช้ `app.metadataCache.getFileCache(file)` เพื่ออ่าน frontmatter, aliases, tags, headings, links และ metadata ที่ Obsidian parse ไว้
>
> รูปแบบหลัก:
>
> ```ts
> const files = app.vault.getMarkdownFiles();
>
> const matches = files.filter((file) => {
>   const cache = app.metadataCache.getFileCache(file);
>   return cache?.frontmatter?.status === 'in-review';
> });
> ```

> [!success]
> ใช้ `MetadataCache` สำหรับ query metadata แทนการอ่านและ parse Markdown/YAML ทุกไฟล์ด้วย regex  
> เหมาะกับ:
>
> - ค้นหา notes ตาม tag
> - ค้นหา notes ตาม `status`
> - ค้นหา notes ตาม `note_type`
> - ค้นหา notes ที่ `reviewed: false`
> - ค้นหา notes ตาม `security_level`
> - ค้นหา notes ตาม aliases
> - สร้าง report/dashboard/graph
> - สร้าง read-only AI agent tools

`Vault.getMarkdownFiles()` คืนรายการ Markdown files ใน vault และ `MetadataCache.getFileCache(file)` คืน parsed metadata ของ note เช่น frontmatter, tags, headings, links, embeds และ blocks [558][579][582][584]

---

## สารบัญ

- [[#ภาพรวม]]
- [[#Basic Pattern]]
- [[#ดึง Markdown Files ทั้งหมด]]
- [[#Filter ตาม Frontmatter Property]]
- [[#Filter ตาม Boolean Metadata]]
- [[#Filter ตาม Tags]]
- [[#Filter ตามหลาย Tags]]
- [[#Filter ตาม Aliases]]
- [[#Filter ตาม Note Type และ Status]]
- [[#Filter ตาม Folder Path]]
- [[#Generic Query Function]]
- [[#Query Builder แบบ Reusable]]
- [[#Performance สำหรับ Vault ขนาดใหญ่]]
- [[#AI Agent Safety]]
- [[#แสดงผลใน Obsidian Modal]]
- [[#Quick Reference]]

---

## ภาพรวม

```text
Obsidian Vault
        │
        ▼
app.vault.getMarkdownFiles()
        │
        ▼
TFile[]
        │
        ▼
app.metadataCache.getFileCache(file)
        │
        ▼
CachedMetadata
        │
        ├── frontmatter
        ├── tags
        ├── aliases
        ├── headings
        ├── links
        ├── embeds
        └── blocks
        │
        ▼
Filter / Sort / Group / Report
Common Use Cases
