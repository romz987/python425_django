from django.http import HttpResponseForbidden
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import User, UserRoles
from reviews.forms import ReviewAdminForm


class ReviewListView(ListView):
    model = Review
    extra_context = {"title": "Все отзывы"}
    template_name = "reviews/reviews.html"

    def get_queryset(self):
        return super().get_queryset().filter(sign_of_review=True)


class ReviewDeactivatedListView(ListView):
    model = Review
    extra_context = {"title": "Неактивные отзывы"}
    template_name = "reviews/reviews.html"

    def get_queryset(self):
        return super().get_queryset().filter(sign_of_review=False)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewAdminForm
    template_name = "reviews/create_update.html"
    extra_context = {"title": "Добавить отзыв"}


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = "reviews/detail.html"
    extra_context = {"title": "Просмотр отзыва"}


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewAdminForm
    template_name = "reviews/create_update.html"
    extra_context = {"title": "Изменить отзыв"}

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset=queryset)
        if object_.author != self.request.user and self.request.user.role not in [
            UserRoles.ADMIN,
            UserRoles.MODERATOR,
        ]:
            raise PermissionDenied()
        return object_

    def get_succuss_url(self):
        return reverse("review:review_detail", args=[self.kwargs.get("slug")])


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review 
    template_name = 'reviews/delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        return reverse('reviews:reviews_list')


def review_toggle_activity(request, slug):
    # 3:28
    review_item = get_object_or_404(Review, slug=slug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False 
        review_item.save() 
        return redirect(reverse('reviews:reviews_deactivated_list'))
    else:
        review_item.sign_of_review = True  
        review_item.save()
        return redirect(reverse('reviews:reviews_list'))
