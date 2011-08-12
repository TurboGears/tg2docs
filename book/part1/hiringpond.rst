=======================================
 Our New Web Application : Hiring Pond
=======================================

As we go through this book, it is helpful to have a goal. In our case,
we will develop an application that is helpful to you, and to the web
community at large. Specifically, we're going to build a resume
hosting site, and the rest of this chapter is devoted to explaining
what it will have, and what it will do for the users of the site.

The site will allow the poster to set up a chronological work history,
complete with bullet points and links to various workplaces. It will
feature a skills matrix, allowing the poster to group related skills
together, and show which skills the poster brings to an employer,
along with a self-rating and experience level for each of those
skills. Finally, each poster will be able to store some specific
successful projects, to showcase ways in which those skills were used
to help an employer.

Each item entered by a poster will be able to be tagged and
cross-tagged. Individual bullet points (under jobs or projects) can be
tagged with skills, as well as tagged with arbitrary other words (such
as "developer" or "sysadmin"). This will allow other users viewing
this resume to follow through and see how different pieces of the
resume interact with each other (which skills were used for a specific
bullet point, for instance, and how does the poster rate himself on
those skills?).

The poster will also have the ability to define a resume as a group of
tags. For instance, the poster may have a "developer" resume and
"systems administrator" resume. While they have overlap, each of these
resumes is meant to showcase something specific to help the poster in
the job search. Using a group of tags as a way to build the resume
allows the poster an easy way to have many different resumes while
only having to maintain the source data once.

Personally identifying information (PII) can be obscured at various
levels: The poster can choose to hide all of it, or to allow names to
be visible, or to allow all to be visible, or other combinations that
are not yet determined.

Users will have an option to request a poster's resume (along with
possibly requesting a specific resume, if the poster chooses to reveal
which resumes are available), and the poster will have the option of
approving or denying the request. If they do approve the request, the
requesting user will receive an email with the resume attached along
with an optional note from the poster.

The poster will be able to easily retrieve any of the resumes that he
has defined in a variety of formats: PDF, HTML, epub, .doc, and .odt
are all possibilities. The poster can choose which of these formats
will be sent to anybody requesting the resume. The poster will be able
to choose which of these formats (if any) are always downloadable by
anybody, including the use of PII on the openly downloadable copy.

The application needs to support two modes: Single poster and multiple
poster. For some posters, it will be desirable to have their personal
domain running a copy of the application for them to promote
themselves. For other posters, they will just want a single site to
host their resume for them. The application should function in both
modes. It should also provide a method to allow single poster sites to
automatically upload entire resumes to multiple poster sites, and
maintain synchronization between the single and multiple poster sites.

The application should, ideally, provide means to upload resumes to
other sites (such as Monster, Dice, Indeed, etc).

In single poster mode, the application should allow the poster to
switch around themes. In multiple poster mode, this is not feasible at
this time.

The application is not LinkedIn: LinkedIn provides profiles, but they
really are not Resume 2.0; rather they are a way to help professionals
connect and stay connnected. The application should provide an option
to update a poster's LinkedIn status, though.

The application is not Monster: Monster provides means to allow
seekers to upload a resume, and then submit that resume to job
postings. The application is not meant to provide job listings in any
way.

This is Hiring Pond: A place for people to cast their resumes out into
the ocean of employers, and see who might be interested in what they
have to offer. If nothing else ever comes of it, they can at least
keep their resume looking good.
