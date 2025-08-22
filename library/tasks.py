from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    overdue_loans = Loan.object.filter(
       is_returned = False,
       due_date = timezone.now().date()
    ).select_related('member__user', 'book')

    for loan in overdue_loans:
        try:
            member_email = loan.member.user.email
            book_title = loan.book.title
            day_overdue = (timezone.now().date() - loan.due_date).days
            send_mail(
                subject=f'OverDue Book Reminder: {book_title}',
                message=f'Hello {loan.member.user.username},\n\nYour Book "{book_title}".\n Is overdue by {day_overdue}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_email],
                fail_silently=False,
            )

        except Exception as e:
            pass
