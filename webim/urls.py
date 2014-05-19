from django.conf.urls import patterns

urlpatterns = patterns('webim.views',
    (r'^$', 'index'),
    (r'^boot$', 'boot'),
    (r'^online$', 'online'),
    (r'^offline$', 'offline'),
    (r'^refresh$', 'refresh'),
    (r'^message$', 'message'),
    (r'^buddies$', 'buddies'),
    (r'^presence$', 'presence'),
    (r'^status$', 'status'),
    (r'^setting$', 'setting'),
    (r'^history$', 'history'),
    (r'^clear_history$', 'clear_history'),
    (r'^download_history$', 'download_history'),
    (r'^room/invite$', 'invite'),
    (r'^room/join$', 'join'),
    (r'^room/leave$', 'leave'),
    (r'^room/block$', 'block'),
    (r'^room/unblock$', 'unblock'),
    (r'^room/members$', 'members'),
    (r'^notifications$', 'notifications'),
    (r'^upload$', 'upload')
)

