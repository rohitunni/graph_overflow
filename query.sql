SELECT TOP 50000 Q.Id as Id, Q.Title as QuestionTitle,
                 Q.Body as QuestionBody, Q.Score as QuestionScore,
                 A.Body as Answer, A.Score as AnswerScore,
                 Q.Tags as Tags

FROM Posts as A

JOIN (SELECT Posts.Id, Posts.Title, Posts.Body, Posts.Tags, Posts.PostTypeId, Posts.Score, Posts.ViewCount, Posts.AcceptedAnswerId
      FROM PostTags
      JOIN Tags ON PostTags.TagId = Tags.Id
      JOIN Posts ON PostTags.PostId = Posts.Id
      WHERE Tags.TagName IN ('python','django','numpy','pandas','python-2.7',
                             'python-3.x','matplotlib','flask','tkinter',
                             'scipy','sqlalchemy', 'scikit-learn',
                             'nltk', 'ipython','ipython-notebook', 'psycopg2')
GROUP BY Posts.Id, Posts.Title, Posts.Body, Posts.Tags, Posts.PostTypeId,
         Posts.Score, Posts.ViewCount, Posts.AcceptedAnswerId) as Q
ON Q.AcceptedAnswerId = A.Id
WHERE Q.Id > ##MinId##
ORDER BY Q.Id ASC

--Min 1: 0
--Min 2:
--Min 3:
--Min 4: 
