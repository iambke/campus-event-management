The assignment was to build a basic campus event management system. From my perspective, the core idea is to connect two sides:

1. The college staff who create and manage events

2. The students who register, attend, and give feedback.

The key flows are event creation, student registration, attendance tracking on the event day, and feedback collection after the event. 

I designed the project in a way that keeps the structure clear and minimal: a small database schema with tables for events, students, registrations, attendance, and feedback; and APIs to perform the main operations around these. The reporting queries are built directly on this data.

The focus for me was not on adding too many extra features, but on making sure the main flow Register → attend → feedback → report, works smoothly and is easy to extend in the future.
