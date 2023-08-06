from django.contrib import admin
from django.utils.translation import pgettext_lazy
from rest_framework_simplejwt.tokens import AccessToken as TokenClass

from .models import Token, TokenUserConnection


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = 'id', 'jti', 'get_token_type', 'parent_id', 'expired_at', 'created_at',
    date_hierarchy = 'created_at'
    autocomplete_fields = 'parent',
    search_fields = 'id', 'jti', 'token', 'user_connections__user__username'
    readonly_fields = (
        'get_token_type', 'get_token_payload',
        'internal_expired_at', 'updated_at', 'created_at',
    )
    fields = (
        'id', 'jti',
        'parent',
        'token',
        'get_token_type',
        'get_token_payload',
        ('expired_at', 'internal_expired_at',),
        ('updated_at', 'created_at',),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).distinct()

    def get_token_payload(self, obj):
        token = TokenClass(obj.token, verify=False)

        return token.payload
    get_token_payload.short_description = pgettext_lazy('wcd_jwt', 'Payload')

    def get_token_type(self, obj):
        payload = self.get_token_payload(obj)

        return payload.get('token_type', '')
    get_token_type.short_description = pgettext_lazy('wcd_jwt', 'Type')


@admin.register(TokenUserConnection)
class TokenUserConnectionAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'token', 'created_at',
    date_hierarchy = 'created_at'
    list_select_related = 'user', 'token',
    autocomplete_fields = 'user', 'token',
    search_fields = 'id', 'user__username', 'token__token', 'token__jti',
    readonly_fields = 'updated_at', 'created_at',
