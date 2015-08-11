.. :changelog:

History
-------


3.0 (in preparation)
++++++++++++++++++++
* ANNOUNCEMENT: In a future release, anonymous users and inactive users are no longer automatically denied every permission. This turns out to be a bad design.


2.5 - In Progress
+++++++++++++++++

* Better code documentation (more to come).
* More tests
* Simplified getting model for an object (get_model_for_perm)
* Removed an unused method for registering permissions


2.4.1 (2014-12-15)
++++++++++++++++++

* Fixed bug in autodiscover


2.5.0 (2015-04-28)
++++++++++++++++++

* Fix Django 1.8 deprecation warning
* Improved stability of checking permission through get_queryset


2.4.0 (2014-12-15)
++++++++++++++++++

* Isolated has_perm in PermSingleObjectMixin


2.3.0 (2014-12-08)
++++++++++++++++++

* Made tests work in Django 1.7
* Modified Travis matrix


2.2.1 (2014-08-28)
++++++++++++++++++

* Fixed bug in `{% ifperm ... %}` tag and added tests


2.2.0 (2014-08-28)
++++++++++++++++++

* New `{% perm ... %}` template tag with optional `as varname` to write to context


2.1.0 (2014-05-21)
++++++++++++++++++

* Must load via urls now, documented this in README


2.0.2 (2014-05-21)
++++++++++++++++++

* Fix Travis CI


2.0.1 (2014-05-21)
++++++++++++++++++

* Now works with standard Django exception PermissionDenied


2.0.0 (2014-05-21)
++++++++++++++++++

* Now works without its own middleware
