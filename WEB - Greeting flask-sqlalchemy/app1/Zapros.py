def main():
    db_name = input().strip()
    global_init(db_name)
    db_sess = create_session()

    department = db_sess.get(Department, 1)
    if not department or not department.members or not department.members.strip():
        return

    member_ids = list(map(int, department.members.strip().split(',')))

    for user in db_sess.query(User).filter(User.id.in_(member_ids)):
        total_hours = 0
        jobs = db_sess.query(Jobs).filter(
            (Jobs.team_leader == user.id) |
            (Jobs.collaborators.like(f'%{user.id}%'))
        ).all()

        for job in jobs:
            is_collab = False
            if job.collaborators:
                collaborators = job.collaborators.split(',')
                collaborators = [c.strip() for c in collaborators]
                is_collab = str(user.id) in collaborators

            if job.team_leader == user.id or is_collab:
                total_hours += job.work_size or 0

        if total_hours >= 25:
            print(f"{user.surname} {user.name}")


if __name__ == "__main__":
    main()